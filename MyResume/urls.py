from django.urls import path

from . import views

urlpatterns =[
    path('', views.aboutme_view, name='about'),
    path('skills/',views.skills_view, name = 'skills'),
    path('qualification/',views.qualification , name='qualification'),
    path('project/',views.project, name='project'),
    path('experience/',views.experience, name='experience'),
    path('contact/',views.contact, name='contact')
]