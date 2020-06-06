from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import ListView, DetailView, FormView, TemplateView

from django.views.generic.edit import UpdateView

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required

from paypal.standard.forms import PayPalPaymentsForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse

from .forms import ClassRegistrationForm, ClassUnregisterForm, ClassPaymentForm, AutoPopulateLessonsForm, ExtPayPalPaymentsForm, PostCreateForm, ClearOldClassesForm

from random import randrange

from .models import Payment, Class

from lessons.models import Lesson

import pythoncamp_project

from posts.models import Post

class ClassListView(ListView):
    template_name = 'classes/list.html'
    model = Class

class ClassDetailView(DetailView):
    template_name = 'classes/detail.html'
    model = Class

class ClassUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'classes/update.html'
    model = Class
    login_url = 'account_login'
    fields = ('name', 'instructor', 'confirmed', 'date', 'end_date', 'start_time', 'end_time', 'first_day', 'second_day', 'third_day_optional','cost','difficulty','description', 'syllabus', )

    def dispatch(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)

class ClassStaffUsersDetailView(DetailView):
    template_name = 'classes/staff_class_user_detail.html'
    model = Class
    login_url = 'account_login'

    

    def dispatch(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)

class StaffListView(LoginRequiredMixin, ListView):
    template_name = 'classes/staff_list.html'
    model = Class
    login_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)

class ClassRegistrationView(LoginRequiredMixin, DetailView, FormView):
    model = Class
    form_class = ClassRegistrationForm
    template_name = 'classes/registration_detail.html'
    # success_url = reverse_lazy('class_list')

    def get_success_url(self):
        return reverse_lazy('class_detail', kwargs={'slug':self.kwargs['slug']})

    login_url = 'account_login'
    
    def form_valid(self, form):
        # query class name from slug (can be changed)
        class_slug = self.kwargs['slug']
        class_ = Class.objects.get(slug=class_slug)
        try: 
            Payment.objects.get(theclass=class_, user=self.request.user)
     
        except:
            payment = Payment(theclass=class_, user=self.request.user, cost=class_.cost)

            payment.save()

        # Class.register(self.request.user, class_)
        return super(ClassRegistrationView, self).form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if obj.past_registration_deadline():
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

class ClassUnregisterView(LoginRequiredMixin, DetailView, FormView):
    model = Class
    form_class = ClassUnregisterForm
    template_name = 'classes/unregister_detail.html'
    # success_url = reverse_lazy('class_list')
    login_url = 'account_login'

    def get_success_url(self):
        return reverse_lazy('class_detail', kwargs={'slug':self.kwargs['slug']})

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if obj.past_registration_deadline():
            raise PermissionDenied
        
        if self.request.user.is_authenticated:
            user_list = self.request.user.classes_paid_list()
            if obj in user_list:
                raise PermissionDenied
        

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        class_slug = self.kwargs['slug']
        class_ = Class.objects.get(slug=class_slug)
        
        # delete the relationship
        try:
            m2 = Payment.objects.get(user=self.request.user, theclass=class_)
            # print("BEEGLEBEEGLE")
            # print(m2.id)
            # print(type(m2.id))
            # for payment in self.request.user.payment_set.all():
            #     print(payment.id) 
            m2.delete()
        except:
            pass
        
        return super(ClassUnregisterView, self).form_valid(form)

class ClearOldClassesView(LoginRequiredMixin, FormView):
    form_class = ClearOldClassesForm
    template_name = 'classes/clear_old_classes.html'
    success_url = reverse_lazy('registered_classes')

    login_url = 'account_login'

       
    def form_valid(self, form):

        try:
            payments = Payment.objects.filter(user=self.request.user, paid=False, theclass__past_payment_deadline=True)
            for payment in payments:
                payment.delete()
        except:
            pass

        return super(ClearOldClassesView, self).form_valid(form)



class ClassPaymentView(LoginRequiredMixin, ListView, FormView):
    model = Class
    form_class = ClassPaymentForm
    template_name = 'classes/payment.html'
    success_url = reverse_lazy('profile')
    login_url = 'account_login'

@login_required
def class_checkout_view(request):

   

    invoice_id = ""
    separator = '|'

    payments = request.user.payments_not_paid_list()
    payment_ids = [str(payment.id) for payment in payments]

    invoice_id = separator.join(payment_ids)

    amount = str(request.user.payment_owed())

    # this is the payment information that paypal will use for redirect
    paypal_dict = {
        "business": pythoncamp_project.settings.PAYPAL_EMAIL,
        "amount": amount,
        "item_name": "name of the item",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('checkout')),
        "cancel_return": request.build_absolute_uri(reverse('checkout')),
   
    }

    
    form = ExtPayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "classes/payment.html", context)

    

class CheckoutSummaryView(LoginRequiredMixin, ListView):
    model = Class
    template_name = 'classes/summary.html'
    login_url = 'account_login'


class RegisteredClassesView(LoginRequiredMixin, TemplateView):
    template_name = 'classes/registered_classes.html'
    login_url = 'account_login'

class PaidClassesView(LoginRequiredMixin, TemplateView):
    template_name = 'classes/paid_classes.html'
    login_url = 'account_login'


class LessonListView(LoginRequiredMixin, DetailView):
    model = Class
    template_name = 'lessons/lesson_overview.html'
    login_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if self.request.user.is_authenticated:
            if not obj in self.request.user.classes_paid_list() and not self.request.user.is_staff:
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class LessonDetailView(LoginRequiredMixin, DetailView):
    login_url = 'account_login'

    def get_object(self):
        pk = self.kwargs['pk']
        slug = self.kwargs['slug']
        # obj = Lesson.objects.get(id=pk, course__slug=slug)
        obj = get_object_or_404(Lesson, id=pk, course__slug=slug)
        print(pk, slug, obj)
        return obj
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if self.request.user.is_authenticated:
            if not obj.course in self.request.user.classes_paid_list() and not self.request.user.is_staff:

                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    template_name = 'lessons/lesson_detail.html'
    


class StaffAutoPopulateField(LoginRequiredMixin, DetailView, FormView):
    form_class = AutoPopulateLessonsForm
    template_name = 'lessons/autopopulate.html'
    model = Class
    success_url = reverse_lazy('lessons_list')
    login_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        
        
        if not self.request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


    def form_valid(self, form):
        class_slug = self.kwargs['slug']
        class_ = Class.objects.get(slug=class_slug)
        num = form.cleaned_data['num']

        Class.auto_populate_courses(class_, num)
        return super(StaffAutoPopulateField, self).form_valid(form)


class LessonUpdateView(LoginRequiredMixin, UpdateView):

    model = Lesson
    template_name = 'lessons/lesson_edit.html'
    def get_success_url(self):
        return reverse_lazy('lesson_detail', kwargs={'slug':self.kwargs['slug'], 'pk':self.kwargs['pk']})
    fields = ('name', 'number', 'active', 'summary',)
    login_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        
        
        if not self.request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class ForumListView(LoginRequiredMixin, DetailView):
    
    model = Class
    template_name = 'posts/post_list.html'
    login_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if self.request.user.is_authenticated:
            if not obj in self.request.user.classes_paid_list() and not self.request.user.is_staff:
                raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

class ForumDetailView(LoginRequiredMixin, DetailView):
    
    def get_object(self):
        pk = self.kwargs['pk']
        slug = self.kwargs['slug']
        # obj = Lesson.objects.get(id=pk, course__slug=slug)
        obj = get_object_or_404(Post, id=pk, course__slug=slug)
        # print(pk, slug, obj)

        return obj
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if self.request.user.is_authenticated:
            if not obj.course in self.request.user.classes_paid_list() and not self.request.user.is_staff:
                raise PermissionDenied
        
            # if obj.author != self.request.user:
            #     raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    template_name = 'posts/post_detail.html'
    login_url = 'account_login'


class ForumUpdateView(LoginRequiredMixin, UpdateView):

    model = Post
    template_name = 'posts/post_edit.html'

    def get_success_url(self):
        return reverse_lazy('forum_detail', kwargs={'slug':self.kwargs['slug'], 'pk':self.kwargs['pk']})

    fields = ('title', 'body')
    login_url = 'account_login'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if self.request.user != obj.author and not self.request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


class ForumCreateView(LoginRequiredMixin, FormView):

    # model = Post
    template_name = 'posts/post_new.html'
    login_url = 'account_login'

    form_class = PostCreateForm

    
    
        
    def form_valid(self, form):
        # title = form.cleaned_data['title']
        # body = form.cleaned_data['body']
        author = self.request.user
        course = get_object_or_404(Class, slug=self.kwargs['slug'])


        # post = Post(title=title, body=body, author=author, course=course)

        form.instance.author = author
        form.instance.course = course
        self.object = form.save()
        

        # form.instance.author = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('forum_detail', kwargs={'slug':self.kwargs['slug'], 'pk':self.object.id,})
    
    def dispatch(self, request, *args, **kwargs):
        
        
        if self.request.user.is_authenticated:
            slug = self.kwargs['slug']
            course = get_object_or_404(Class, slug=slug)
            if not course in self.request.user.classes_paid_list() and not self.request.user.is_staff:
                raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

