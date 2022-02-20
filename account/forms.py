from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import fields

from .models import User, Profile

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
BLOOD_GROUP = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, help_text="Required.")

    class Meta:
        model = User
        fields=('email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = User.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already in use!!!")


class AccountAuthenticationForm(forms.ModelForm):
    
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")

class ProfileForm(forms.ModelForm):
    class meta:
        model = Profile
        fields=('first_name', 'last_name', 'phone_no', 'address', 'age', 'gender', 'blood_group')

class UdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('date_of_birth',)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'phone_no', 'address', 'age', 'gender', 'blood_group', 'physically_disabled')

class LoginForm(forms.Form):
    email = forms.EmailField(max_length=256)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)