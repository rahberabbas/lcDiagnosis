from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls.base import reverse
from .forms import RegistrationForm, UpdateProfileForm, LoginForm
from django.contrib import messages
from .models import MainUser, Profile
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from .models import User
import threading

MUser = settings.AUTH_USER_MODEL

class EmailThread(threading.Thread):
    
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def login_view(request):
    message = ''
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if not user.is_email_verified:
            message = "Email is not  verified. Please check inbox and spam box."
            return render(request, 'account/login.html', {'message': message})
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'account/login.html')


def logout_request(request):
    logout(request)
    return redirect('register')

def login_request(request):
    form = LoginForm()
    message = ''
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if not user.is_email_verified:
                message = "Email is not  verified. Please check inbox and spam box."
                return render(request, 'account/login2.html', {'message': message})
            if user is not None:
                login(request, user)
                message = f'Hello! You have been logged in'
                return redirect('editprofile')
            else:
                message = 'Invalid Email and Password!'
        else:
            message = 'Invalid Email and Password!'
    return render(
        request, 'account/login2.html', context={'form': form, 'message': message})

def login_requ(request):
    if request.method == "POST":
        
        form = LoginForm(request.POST)
        message = ''
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(
                email=email,
                password=password,
            )
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in.")
                print("Yes")
                return redirect("editprofile")
            else:
                message = "Invalid username or password."
                print("No")
        else:
            message = "Invalid username or password."
            print("Wrong")
    form = LoginForm()
    return render(request=request, template_name="account/login.html", context={"login_form":form, 'message': message})

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from .tokens import generate_token
from django.core.mail import EmailMessage

def send_action_email(user, request):
    current_site = get_current_site(request)
    emaill_subject = 'Activate your account'
    email_body = render_to_string('activation_request.html',{
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=emaill_subject, body=email_body, from_email=settings.EMAIL_HOST_USER, to=[user])
    if not settings.TESTING:
        EmailThread(email).start()

def register_view(request, *args, **kwargs):
    user = request.user
    if user.is_authenticated: 
        return redirect('/')

    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        profile = UpdateProfileForm(request.POST)
        if form.is_valid():
            userr = form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            # login(request, account)
            account.save()
            # account.refresh_from_db()
            
            send_action_email(userr, request)

            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect(reverse('activtaion_send'))
        else:
            message = messages.error(request, 'Something is Wrong')
            context['registration_form'] = form
            context['profile_form'] = profile

    else:
        form = RegistrationForm()
        profile = UpdateProfileForm()
        context['registration_form'] = form
    return render(request, 'account/register2.html', {'form': form})

def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        message = 'Email Verified'
        return redirect('login')
    return render(request, 'activate_failed.html', {'user': user})

def get_redirect_if_exists(request):
    redirect = None
    if request.GET:
	    if request.GET.get("next"):
		    redirect = str(request.GET.get("next"))
    return redirect

def activtaion_send(request):
    return render(request, 'activation_sent.html')

@login_required(login_url='/login/')
def profile(request):
    profile = Profile.objects.filter(user=request.user)
    return render(request, 'dashboard/profile.html', {'profile': profile})

@login_required(login_url='/login/')
def editprofile(request):
    if request.method == "POST":
        print('working')
        # u_form = 
        p_form = UpdateProfileForm(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            # custom_form = p_form.save(False)
            # custom_form.save()
            p_form.save()

    else:
        p_form = UpdateProfileForm(instance=request.user.profile)
        print("incorrect")
    return render(request, 'dashboard/editprofile.html', {'Pform': p_form})

@login_required(login_url='/login/')
def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/changepass.html', {
        'form': form
    })

from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('link')


def login2(request):
    form = LoginForm()
    message = ''
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if not user.is_email_verified:
                message = "Email is not  verified. Please check inbox and spam box."
                return render(request, 'account/login2.html', {'message': message})
            if user is not None:
                login(request, user)
                message = f'Hello! You have been logged in'
                return redirect('editprofile')
            else:
                message = 'Invalid Email and Password!'
        else:
            message = 'Invalid Email and Password!'
    return render(
        request, 'account/login2.html', context={'form': form, 'message': message})
    # return render(request, 'account/login2.html')

def link(request):
    return render(request, 'account/link.html')