from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url


urlpatterns = [
	url(r'^recommendations/', views.recommendation),
    url(r'^simrecommendations/', views.get_suggestions),
	path('anything/',views.anything,name="related"),
	path('related/',views.related,name="related"),
    path('related/<int:movie_id>',views.related,name="related"),
    path('', views.index),
	path('login_page/', views.login_page),
	path('signup_page/', views.signup_page),
	path('accounts/login/', views.login_page),
	path('accounts/signup/', views.signup_page),
	path('signup/', views.signup),
	path('login/', views.login),
	path('logout/', views.logout_view),
	path('profile/', views.profile),
	#path('profilepicture/', views.profilepicture),
	path('updateprofile/', views.updateprofile),
	path('search/', views.search),
	#path('upload/', views.upload),
	path('signup/', views.signup),
	path('create_post/', views.create_post),
	#path('list_post/', views.list_post),
	path('detail_post/<str:pk>/', views.detail_post , name="detail_post"),
	path('update_post/<str:pk>/', views.update_post),
	path('delete_post/<str:pk>/', views.delete_post),
	path('passwordchange/', views.passwordchange),
	path('addreview/<str:pk>/', views.addreview, name="addreview"),
	# milena vanii yo tala ko line with base.html del

	path('passwordreset/', auth_views.PasswordResetView.as_view(template_name="password_reset_form.html"), name="reset_password"),
	path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name="password_reset_done"),
	path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
	path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete")
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

