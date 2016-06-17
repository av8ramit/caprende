"""caprende URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from allauth.account.views import confirm_email

from analytics import views as analytics_views
from categories import views as categories_views
from comments import views as comment_views
from contact import views as contact_views
from course import views as course_views
from questions import views as question_views
from users import views as users_views

from .views import home

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
]

#allauth accounts URLS
urlpatterns += [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^verify-email/(?P<key>\w+)/$', confirm_email, name="account_confirm_email"),
]

#user model URLS
urlpatterns += [
    url(r'^edit_profile/$', users_views.edit_profile, name='edit_profile'),
]

#categories model URLS
urlpatterns += [
    url(r'^category/(?P<slug>[\w-]+)/$', categories_views.category_detail, name='category_detail'),
    url(r'^subcategory/(?P<slug>[\w-]+)/$', categories_views.subcategory_detail, name='subcategory_detail'),
]

#comments model URLS
urlpatterns += [
    url(r'^comment/(?P<comment_id>\d+)/$', comment_views.comment_thread, name='comment_thread'),
    url(r'^comment/create/$', comment_views.comment_create_view, name='comment_create'),
]

#contact model URLS
urlpatterns += [
    url(r'^contact_us/$', contact_views.contact_us, name='contact_us'),
]

#course model URLS
urlpatterns += [
    url(r'^courses/$', course_views.course_list, name='course_list'),
    url(r'^course/(?P<slug>[\w-]+)/$', course_views.course_detail, name='course_detail'),
]

#question model URLS
urlpatterns += [
    url(r'^question/(?P<course>[\w-]+)/(?P<question_id>\d+)/(?P<response>\w)/$', question_views.question_review, name='question_review'),
    url(r'^question/(?P<course>[\w-]+)/(?P<question_id>\d+)/$', question_views.question_detail, name='question_detail'),

]

#analytics model URLS
urlpatterns += [
    url(r'^dashboard/$', analytics_views.dashboard, name='dashboard'),
]

#static file imports
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
