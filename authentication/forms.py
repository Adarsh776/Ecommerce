from django import forms
from .models import Custom_UserModel
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class Custom_UserForm(UserCreationForm):
    class Meta:
        model=Custom_UserModel
        fields=['username','first_name','last_name','gender','date_of_birth','email','phone','password1','password2']
        widgets={
            'gender':forms.RadioSelect(),
            'date_of_birth':forms.DateInput(attrs={'type':'date'})
        }

        lables={
            'phone':'Phone no',
            'gender':'Gender',
            'date_of_birth':'Date of Birth'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['gender'].choices = [
            ('male', 'Male'),
            ('female', 'Female')
        ]
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

class IdentifyUserForm(forms.Form):
    UsernameorEmail=forms.CharField(max_length=100, label="Username or Email", widget=forms.TextInput(attrs={'placeholder': 'Enter username or email'}))

class VerifyOtpForm(forms.Form):
    Otp=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Otp'}))




    
