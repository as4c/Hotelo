from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

# User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    name = forms.CharField(required=True, label=_("Name"))
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=True, label=_("Phone"))
    gender = forms.ChoiceField(required=False, choices=GENDER_CHOICES, label=_("Gender"))
    age = forms.IntegerField(required=False, label=("Age"))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':3}), label=_("Address"))
    profile_image = forms.ImageField(required=False, label=_("Profile Image"))
    

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + ('name','email', 'phone','profile_image', 'gender', 'age', 'address')


class UserEditForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    name = forms.CharField(required=True, label=_("Name"))
    phone = forms.CharField(required=True, label=_("Phone"))
    gender = forms.ChoiceField(required=False, choices=GENDER_CHOICES, label=_("Gender"))
    age = forms.IntegerField(required=False, label=_("Age"))
    address = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':3}), label=_("Address"))
    profile_image = forms.ImageField(required=False, label=_("Profile Image"))

    class Meta:
        model = get_user_model()
        fields = ('name', 'phone', 'profile_image', 'gender', 'age', 'address')


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if email:
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("This email is not registered.")
            return user.username
        raise forms.ValidationError("Please enter an email address.")
