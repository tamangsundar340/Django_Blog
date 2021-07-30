from django.db import models
from django.contrib.auth.models import Group,User
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse


# Create your models here.        
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    update_at  = models.DateTimeField(auto_now=True)
    is_active  = models.BooleanField(default=True, null=True, blank=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        self.update_at = timezone.now()
        return super().save(*args, **kwargs)
    
    def timestamp_pretty(self):
        return self.created_at.strftime('%b %e, %Y')


class SiteAdmin(TimeStamp):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    name  = models.CharField(max_length=50)
    image = models.ImageField(upload_to="user/SiteAdmin", null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        group, group_created = Group.objects.get_or_create(name="SiteAdmin")
        self.user.groups.add(group)
        super().save(*args, **kwargs)
        

class Member(TimeStamp):
    user           = models.OneToOneField(User, on_delete=models.CASCADE)
    name           = models.CharField(max_length=200)
    image          = models.ImageField(upload_to="user/member", null=True, blank=True)
    mobile         = models.CharField(max_length=200, null=True, blank=True)
    street_address = models.CharField(max_length=200, null=True, blank=True)
    
    def getFullName(self):
        return self.user.first_name + ' ' + self.user.last_name

    def save(self, *args, **kwargs):
        group, group_create = Group.objects.get_or_create(name="Member")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

        
class SiteInformation(TimeStamp):
    title                   = models.TextField(max_length=50, blank=True, null=True)
    email                   = models.EmailField()
    phone_number            = models.PositiveIntegerField(blank=True, null=True)
    address                 = models.TextField(max_length=200, blank=True, null=True)
    profile_image           = models.ImageField(upload_to="profile/pic", null=True, blank=True)
    about_us                = models.TextField(blank=True, null=True)
    github                  = models.CharField(max_length=200,null=True,blank=True)
    facebook                = models.CharField(max_length=200,null=True,blank=True)
    instagram               = models.CharField(max_length=200,null=True,blank=True)
    youtube                 = models.CharField(max_length=200,null=True,blank=True)
    twitter                 = models.CharField(max_length=200,null=True,blank=True)
    viber                   = models.CharField(max_length=200,null=True,blank=True)
    privacy_policy          = models.TextField(blank=True, null=True)
    terms_conditions        = models.TextField(blank=True, null=True)
    fb_messenger_script     = models.CharField(max_length=1024, null=True, blank=True)
    google_analytics_script = models.CharField(max_length=500, null=True, blank=True)
    fb_pixel_script         = models.CharField(max_length=4000, null=True, blank=True)
    detail_pixel            = models.TextField(null=True, blank=True)
    

class Notice(TimeStamp):
    title         = models.CharField(max_length=150)
    content       = models.TextField()
    
    
class ContactMessage(TimeStamp):
    fullname      = models.CharField(max_length=100,null=True, blank=True)
    email         = models.EmailField(null=True, blank=True)
    subject       = models.CharField(max_length=250,null=True, blank=True)
    message       = models.TextField()

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name_plural = "ContactMessages"
    

class Category(TimeStamp):
    title = models.CharField(max_length=20)
    slug  = models.SlugField(null=True, blank=True, unique=True)

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

    

class Blog(TimeStamp):
    title      = models.CharField(max_length=100)
    slug       = models.SlugField(null=True, blank=True, unique=True)
    overview   = models.TextField()
    content    = models.TextField()
    views      = models.PositiveIntegerField(default=0)
    author     = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    thumbnail  = models.ImageField(upload_to="Blog/img")
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)
    featured   = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absoulate_url(self):
        return reverse('core:blogdetail',kwargs ={
            'slug':self.slug
        })
        
    def comment_count(self):
        return BlogComment.objects.filter(blog=self).count()
    
class BlogComment(TimeStamp):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=True, max_length=50)
    text = models.TextField(max_length=200)
    reply = models.ForeignKey("self", on_delete=models.CASCADE,
        null=True, blank=True, related_name="replies")

    def __str__(self):
        return f"By: ({self.name}) for ({self.blog})."
    
    
    
# Newsletter
class Newsletter(TimeStamp):
    email     = models.EmailField()

    def __str__(self):
        return self.email
    
    
    
