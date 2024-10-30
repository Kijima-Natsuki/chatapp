from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import CustomUser, Message

User = get_user_model()

class SignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_image', "password1", "password2"]
        widgets = {
            'profile_image': forms.FileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def signup(self, user):
        user.email = self.cleaned_data['email']
        profile_image = self.cleaned_data.get('profile_image')
        if profile_image is not None:
            user.profile_image = profile_image
        user.save()

class LoginForm(AuthenticationForm):
    pass

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 1, 'style': 'width: 40vh;'})
        }
        labels = {
            'content': ''
        }

class UserImageUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.FileInput(),
        }

class UsernameUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']

class UserEmailUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']