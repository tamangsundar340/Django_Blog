from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from core.models import Blog, Category, BlogComment, ContactMessage, Newsletter
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.contrib import messages

# for mailchimp
from django.conf import settings
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from django.http import HttpResponseRedirect
import json
import requests



# Create your views here.
def count():
    category = Category.objects.annotate(count_post = Count('blog'))
    return category

class homeView(ListView):
    template_name = "clienttemplate/index.html"
    model = Blog
    paginate_by = "2"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bloglist = Blog.objects.all().order_by('-id')
        paginator = Paginator(bloglist, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['bloglist'] = file_exams
        
        context["trending_blogs"] = Blog.objects.all().order_by('-views')[:3]
        context['categories'] =  count()
        return context



class BlogListView(TemplateView):
    template_name = "clienttemplate/bloglist.html"
    paginate_by = "5"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bloglist = Blog.objects.all().order_by('-id')
        paginator = Paginator(bloglist, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        context['bloglist'] = file_exams
        
        context["trending_blogs"] = Blog.objects.all().order_by('-views')[:3]
        context['categories'] =  count()
        return context

class BlogDetalView(TemplateView):
    template_name = "clienttemplate/blog-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogobj = Blog.objects.get(slug = self.kwargs['slug'])
        blogobj.views += 1
        blogobj.save()
        context["trending_blogs"] = Blog.objects.all().order_by('-views')[:3]
        context['categories'] =  count()
        context['blogdetail'] = blogobj
        context["comments"] = BlogComment.objects.filter(blog=blogobj) 
        return context
    
    def post(self, request, *args, **kwargs):
        blog = Blog.objects.get(slug = self.kwargs['slug'])
        name = self.request.POST['name']
        text = self.request.POST['text']
        if name !="" and text !="":
            try:
                blog_obj          = BlogComment()
                blog_obj.name     = name
                blog_obj.text     = text
                blog_obj.blog     = blog
                blog_obj.save()
                return JsonResponse({'status':'ok'})
            except ObjectDoesNotExist:
                return JsonResponse({'status':'error'})
        else:
            return JsonResponse({'status':'error'})

class CategoryView(TemplateView):
    template_name = "clienttemplate/category.html"
    paginate_by = "5"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogCategory = Category.objects.get(slug = self.kwargs['slug'])
        order_qs = Blog.objects.all().filter(categories=blogCategory)
        context['blogCategory'] = blogCategory
        context['cate'] = order_qs
        context['categories'] =  count()
        paginator = Paginator(order_qs, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            file_exams = paginator.page(page)
        except PageNotAnInteger:
            file_exams = paginator.page(1)
        except EmptyPage:
            file_exams = paginator.page(paginator.num_pages)
        
        context["trending_blogs"] = Blog.objects.all().order_by('-views')[:3]
        return context


class ContactView(TemplateView):
    template_name = "clienttemplate/contact.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
        
    def post(self, request, *args, **kwargs):
        fullname = self.request.POST['fullname']
        email = self.request.POST['email']
        subject = self.request.POST['subject']
        message = self.request.POST['message']
        if fullname !="" and email !="" and subject != "" and message != "":
            try:
                contact_obj              = ContactMessage()
                contact_obj.fullname     = fullname
                contact_obj.email        = email
                contact_obj.subject      = subject
                contact_obj.message      = message
                contact_obj.save()
                return JsonResponse({'status':'ok'})
            except ObjectDoesNotExist:
                return JsonResponse({'status':'error'})
        else:
            return JsonResponse({'status':'error'})
        



# Email subscription
# Mailchimp Settings
api_key = settings.MAILCHIMP_API_KEY
server = settings.MAILCHIMP_DATA_CENTER
list_id = settings.MAILCHIMP_EMAIL_LIST_ID

def subscribe(email):
    """
    Contains code handling the communication to the mailchimp api
    to create a contact/member in an audience/list.
    """

    mailchimp = Client()
    mailchimp.set_config({
        "api_key": api_key,
        "server": server,
    })

    member_info = {
        "email_address": email,
        "status": "subscribed",
    }

    try:
        response = mailchimp.lists.add_list_member(list_id, member_info)
        print("response: {}".format(response))
    except ApiClientError as error:
        print("An exception occurred: {}".format(error.text))
        
        
def SubscribeView(request):
    if request.method == "POST":
        try:
            email = request.POST['email']
            email_signup_qs = Newsletter.objects.filter(email=email)
            if email_signup_qs.exists():
                return JsonResponse({'status':'already'})
            else:
                newsletter              = Newsletter()
                newsletter.email        = email
                subscribe(email)
                newsletter.save()
                return JsonResponse({'status':'ok'})
        except:
            return JsonResponse({'status':'error'})
    else:
        print("Not a post method.......")