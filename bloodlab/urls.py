from django.contrib import admin
from django.urls import path
from account.views import login_view, register_view, logout_request, profile, editprofile, changepass, login_request, ResetPasswordView, activate_user, activtaion_send
from core.views import index, Import_csv, products, ProductDetailView, add_to_cart, show_cart, removecart, checkout, payment_done, order, contact, about, service, covid
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_request, name='login'),
    path('register/', register_view, name='register'),
    path('activate-user/<uidb64>/<token>', activate_user, name='activate'),
    path('activate-send', activtaion_send, name='activtaion_send'),
    path('', index, name='index'),
    path('contact/', contact, name='contact'),
    path('covid-updates/', covid, name='covid'),
    path('about-us/', about, name='about'),
    path('our-services/', service, name='service'),
    path('lab-test/', products, name='products'),
    path('logout/', logout_request, name='logout'),
    path('Import_csv/', Import_csv,name="Import_csv"), 
    path('detail/<int:pk>', ProductDetailView.as_view(),name="detail"), 
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', show_cart, name='showcart'),
    path('removecart/', removecart),
    path('checkout/', checkout, name='checkout'),
    path('payment-done/', payment_done, name='payment_done'),
    path('order/', order, name='order'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', editprofile, name='editprofile'),
    path('chnage-password/', changepass, name='changepass'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
]



# Admin Panel