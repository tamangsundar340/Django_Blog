from core.models import Category
from django.urls import path
from .views import (
    homeView,
    BlogListView,
    ContactView,
    BlogDetalView,
    CategoryView,
    SubscribeView,
)
app_name = 'core'

urlpatterns = [
    path('', homeView.as_view(),name='home'),
    path('bloglist/', BlogListView.as_view(),name='bloglist'),
    path('blogdetail/<slug>/', BlogDetalView.as_view(),name='blogdetail'),
    path('category/<slug>/', CategoryView.as_view(),name='category'),
    path('subscribe/', SubscribeView, name='subscribe'),
    path('contact/', ContactView.as_view(),name='contact'),
]