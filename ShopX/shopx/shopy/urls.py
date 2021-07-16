from re import S, template
from django.urls import path
from shopy import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import authenticate, views as auth_view #import LoginView, logoutView
from .form import (
    LoginForm, 
    MyPasswordChangeForm, 
    MyPasswordResetForm,
    MySetPasswordForm, 
    SetPasswordForm
)


urlpatterns = [

    # path('', views.home),
    #home_page
    path('',
        views.ProductView.as_view(),
        name='homi'),
    
    #detail_page
    path('product-detail/<int:pk>',
        views.ProductDetailView.as_view(),
        name='product-detail'),

    path('add-to-cart/',
        views.add_to_cart, 
        name='add-to-cart'),

    path('cart/', 
        views.show_cart, 
        name="showcart"),
    
    path('pluscart/', 
        views.plus_cart),
    
    path('minuscart/', 
        views.minus_cart),

    path('removecart/', 
        views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),

    path('profile/',
         views.ProfileView.as_view(),
         name='profile'
    ),


    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    # change_Pass _page
    path('changepassword/',
        auth_view.PasswordChangeView.as_view(template_name='shopy/passwordchange.html',
        form_class = MyPasswordChangeForm, success_url='/changepwddone/'),
        name='changepassword'),

    path('changepwddone/',
        auth_view.PasswordChangeDoneView.as_view(
        template_name='shopy/changepwdddone.html'),
        name='changepwddone'),

    path('password-reset/',
         auth_view.PasswordResetView.as_view(template_name='shopy/resetpassword.html',
        form_class=MyPasswordResetForm) ,
        name='password_reset'), 
    
    path('password-reset-done/', 
        auth_view.PasswordResetDoneView.as_view(template_name='shopy/resetpassworddone.html'),
        name='password_reset_done'), 

    path('password-reset-confirm/<uidb64>/<token>/', 
        auth_view.PasswordResetConfirmView.as_view(template_name='shopy/resetpasswordcomfirm.html',
        form_class=MySetPasswordForm) ,
        name='password_reset_confirm'),
    
    path('password-reset-complete/', 
        auth_view.PasswordResetCompleteView.as_view(template_name='shopy/resetpasswordcomplete.html'),
        name='password_reset_complete'), 

    path('mobile/',
        views.mobile, 
        name='mobile'),

    path('mobile/<slug:data>', 
        views.mobile, 
        name='mobiledata'),

    path('acounts/login/', 
        auth_view.LoginView.as_view(template_name='shopy/login.html',authentication_form=LoginForm), 
        name='login'),

    path('logout/', 
        auth_view.LogoutView.as_view(next_page='login'), 
        name='logout'),

    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', 
        views.CustomerRegistrationView.as_view(),  
        name='customerregistration'),
    
    #checkput_page
    path('checkout/',
         views.checkout, 
         name='checkout'),

    path('paymentdone', 
        views.payment_done,
        name='paymentdone')

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)