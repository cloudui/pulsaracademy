from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import ListView, DetailView, FormView, TemplateView

from django.views.generic.edit import UpdateView, DeleteView, CreateView

from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required

from paypal.standard.forms import PayPalPaymentsForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy, reverse

from .forms import (
    ClassRegistrationForm, 
    ClassUnregisterForm, 
    AutoPopulateLessonsForm,
     ExtPayPalPaymentsForm, 
     PostCreateForm, 
     ClearOldClassesForm, 
     PostDeleteForm,
     IntroFormView,
)
from django.http import JsonResponse, HttpResponse
import json

from random import randrange

from .models import Payment, Class, Introduction

from lessons.models import Lesson

import pythoncamp_project

from posts.models import Post, Comment

class ClassListView(ListView):
    template_name = 'classes/list.html'
    model = Class

class ClassCreateView(CreateView):
    template_name = 'classes/create.html'
    model = Class
    fields = ('__all__', )

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

class ClassUnregisterCartView(LoginRequiredMixin, DetailView, FormView):
    model = Class
    form_class = ClassUnregisterForm
    template_name = 'classes/unregister_cart_detail.html'
    # success_url = reverse_lazy('class_list')
    login_url = 'account_login'

    def get_success_url(self):
        return reverse_lazy('summary')

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
        
        return super(ClassUnregisterCartView, self).form_valid(form)

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



@login_required
def class_checkout_view(request):

   

    invoice_id = ""
    separator = '|'

    payments = request.user.payments_pay_now()
    payment_ids = [str(payment.id) for payment in payments]

    for payment in payments:
        print(payment.theclass)

    invoice_id = separator.join(payment_ids)

    amount = str(request.user.payment_owed())

    # this is the payment information that paypal will use for redirect
    paypal_dict = {
        "business": pythoncamp_project.settings.PAYPAL_EMAIL,
        "amount": amount,
        "item_name": "PA Courses",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('checkout')),
   
    }

    
    form = ExtPayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    print(invoice_id, amount )
    print("BEEGLEBEEGLEBEEGLE")
    return render(request, "classes/payment.html", context)

    

def class_specific_checkout_view(request, slug):

    class_ = Class.objects.get(slug=slug)
    
    payment = get_object_or_404(Payment, theclass__slug=slug, theclass__confirmed=True, theclass__past_payment_deadline=False, paid=False, user=request.user)

    invoice_id = ""
    # separator = '|'

    

    invoice_id = payment.id

    amount = str(class_.cost)

    # this is the payment information that paypal will use for redirect
    paypal_dict = {
        "business": pythoncamp_project.settings.PAYPAL_EMAIL,
        "amount": amount,
        "item_name": "PA Courses",
        "invoice": invoice_id,
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('checkout')),
   
    }

    
    form = ExtPayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form, 'object': class_
    
    }
    print(invoice_id, amount, )
    return render(request, "classes/individual_checkout.html", context)


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
    def get_success_url(self):
        return reverse_lazy('lesson_list', kwargs={'slug':self.kwargs['slug']})
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
    fields = ('name', 'number', 'active', 'summary', 'homework',)
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

class ForumDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'posts/post_delete.html'
    
    model = Post

    login_url = 'account_login'
    def get_success_url(self):
        return reverse_lazy('forum_list', kwargs={'slug':self.kwargs['slug'],})

    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if self.request.user != obj.author and not self.request.user.is_staff:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

class PaymentSuccessView(TemplateView):
    template_name = 'classes/payment_successful.html'


class ClassIntroView(LoginRequiredMixin, DetailView):

    login_url = 'account_login'

    template_name = 'lessons/intro.html'
    model = Class

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if self.request.user.is_authenticated:
            if not obj in self.request.user.classes_paid_list() and not self.request.user.is_staff:
                raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)
    
class ClassIntroUpdateView(LoginRequiredMixin, UpdateView):

    
    template_name = 'lessons/intro_edit.html'
    login_url = 'account_login'
    fields = ('title', 'body')

    def get_success_url(self):
        return reverse_lazy('lesson_intro', kwargs={'slug':self.kwargs['slug']})

    def dispatch(self, request, *args, **kwargs):
        
        if self.request.user.is_authenticated:
            if not self.request.user.is_staff:
                raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        
        obj = get_object_or_404(Class, slug=self.kwargs['slug'])
        return obj.introduction
    

# class AjaxableResponseMixin:
#     """
#     Mixin to add AJAX support to a form.
#     Must be used with an object-based FormView (e.g. CreateView)
#     """
#     def form_invalid(self, form):
#         response = super().form_invalid(form)
#         if self.request.is_ajax():
#             return JsonResponse(form.errors, status=400)
#         else:
#             return response

#     def form_valid(self, form):
#         # We make sure to call the parent's form_valid() method because
#         # it might do some processing (in the case of CreateView, it will
#         # call form.save() for example).
#         response = super().form_valid(form)
#         if self.request.is_ajax():
#             data = {
#                 'pk': self.object.pk,
#             }
#             return JsonResponse(data)
#         else:
#             return response
class CommentCreateView(LoginRequiredMixin, CreateView):

    template_name = 'posts/comment_new.html'  
    model = Comment
    fields = ('body',)

    

    def get_success_url(self):
        return reverse_lazy('forum_detail', kwargs={'slug':self.kwargs['slug'], 'pk':self.kwargs['pk'],})
    
    def form_valid(self, form):
        
        user = self.request.user
        course = get_object_or_404(Class, slug=self.kwargs['slug'])

        post = get_object_or_404(Post, course=course)

       

        form.instance.user = user
        form.instance.post = post
        # form.instance.course = course
        self.object = form.save()
        

        # form.instance.author = self.request.user
        return super().form_valid(form)

class OldCommentCreateView(LoginRequiredMixin, FormView):

    template_name = 'posts/comment_new.html'  
    model = Comment
    fields = ('body',)

    

    # def get_success_url(self):
    #     return reverse_lazy('forum_detail', kwargs={'slug':self.kwargs['slug'], 'pk':self.kwargs['pk'],})

    
    
    def form_invalid(self, form):
        response = super(CommentCreateView, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    
    def form_valid(self, form):
        
        user = self.request.user
        course = get_object_or_404(Class, slug=self.kwargs['slug'])

        post = get_object_or_404(Post, course=course)

        
        if self.request.is_ajax():
            response_data = {}
        
            body = self.request.POST.get('body')
        
            comment = Comment(user=self.request.user, post=post, body=body)
            comment.save()
            self.object = comment 
        
            response_data['body'] = comment.body
            response_data['user'] = comment.user
            response_data['post'] = comment.post
            response_data['date'] = comment.date.strftime('%B %d, %Y %I:%M %p')
            response_data['date_updated'] = comment.date_updated.strftime('%B %d, %Y %I:%M %p')

            return JsonResponse(response_data)
        

        else:

            form.instance.user = user
            form.instance.post = post
            
            self.object = form.save()
                     
            return super().form_valid(form)

def create_comment(request, slug, pk):
    print('called')
    if request.method == 'POST':
        response_data = {}
        body = request.POST.get('body')
        course = get_object_or_404(Class, slug=slug)

        post = get_object_or_404(Post, course=course, id=pk)
        
        comment = Comment(user=request.user, post=post, body=body)
        comment.save()
        
        
        response_data['body'] = comment.body
        response_data['user'] = comment.user.first_name
        response_data['post'] = comment.post.title
        response_data['date'] = comment.date.strftime('%B %d, %Y %I:%M %p')
        response_data['date_updated'] = comment.date_updated.strftime('%B %d, %Y %I:%M %p')
        print('biggaya')
        print('biggaye')
        return JsonResponse(response_data)
            
    else:
        
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

class ClassScheduleView(TemplateView):
    template_name = 'classes/schedule.html'
   

