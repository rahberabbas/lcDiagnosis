from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.dispatch import receiver 
from django.db.models.signals import post_save 
from django.core.validators import RegexValidator


MainUser = settings.AUTH_USER_MODEL

class UserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email = UserManager.normalize_email(email),
            date_of_birth = date_of_birth
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        u = self.create_user(email,
                        password=password,
                        date_of_birth=date_of_birth
                    )
        u.is_admin = True
        u.save(using=self._db)
        return u

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=256, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects =  UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
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
    user = models.OneToOneField(MainUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, null=True)
    phone_regex = RegexValidator( regex = r'^\d{10}$',message = "phone number should exactly be in 10 digits")
    phone_no = models.CharField(max_length=12, validators=[phone_regex], null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    age = models.CharField(max_length=256, null=True, blank=True)
    physically_disabled = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP, null=True, blank=True)

    def __str__(self):
        return self.user.email

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
	    if created:
		    Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
	    instance.profile.save()
