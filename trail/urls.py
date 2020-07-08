from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [path('',views.home,name='home'),
               path('singlebarvisualizer/',views.singlebarvisualizer,name = 'singlebarvisualizer'),
               path('circlevisualizer/',views.circlevisualizer,name = 'circlevisualizer'),
               path('normalvisualizer/',views.normalvisualizer,name='normalvisualizer'),
               path('publicsongvisualizer/',views.publicsongvisualizer,name='publicsongvisualizer'),
               path('mylistvisualizer/',views.mylistvisualizer,name='mylistvisualizer'),
               path('combinedvisualizer/',views.combinedvisualizer,name='combinedvisualizer'),
                path('upload/',views.upload,name='upload'),
                path('mylist/',views.mylist,name='mylist'),
                path('publicsongs/',views.publicsongs,name='publicsongs'),
                path('searchpublicsong/',views.searchpublicsong,name='searchpublicsong'),
                path('searchmylist/',views.searchmylist,name='searchmylist'),
                path('deletemylist/',views.deletemylist,name='deletemylist'),
                path('compare/',views.compaare,name='compare'),
               path('combine',views.combine,name='combine'),
               path('song',views.song,name='song'),
               path('recorder',views.recorder,name='recorder'),
               path('save',views.save,name='save'),
               path('accounts/signup/', views.signup, name='signup'),
			   path('accounts/login/', views.login, name='login'),
			   path('accounts/reset_password/', auth_views.PasswordResetView.as_view(template_name='forgot_password.html'), name='reset_password'),
			   path('accounts/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
			   path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_form.html'), name='password_reset_confirm'),
			   path('accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
			   path('accounts/logout/', views.logout, name='logout')]

