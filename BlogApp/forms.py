from django import forms
from .models import Post,Author,UserOtp
from django_recaptcha.fields import ReCaptchaField
from django.contrib.auth.models import User
import datetime

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [  
            'description',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }

   
class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ["name", "bio", "facebook",'twitter','instagram','other','image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter a short bio', 'rows': 3}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Facebook profile URL'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Twitter profile URL'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Instagram profile URL'}),
            'other': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Other profile URL'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
    def clean_name(self):
        print("ia m here")
        name = self.cleaned_data.get('name')
        if not all(c.isalpha() or c.isspace() or c in "-_" or c.isdigit() for c in name):
            raise forms.ValidationError('Name can only contain letters, numbers, spaces, hyphens, and underscores.')
        return name


class LoginForm(forms.Form):
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    captcha = ReCaptchaField()



class RegisterForm(forms.Form):
    name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'})
    )
    captcha = ReCaptchaField()


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already associated with another user.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

    def save(self):
        # Extract the data from cleaned_data
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        # Create a username using the name and a timestamp
        suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
        username_datefield = "_".join([name, suffix])
        
        # Create the user instance with the hashed password
        user = User(username=username_datefield, email=email,first_name=name,is_active=False)
        user.set_password(password)  # This ensures the password is hashed
        user.save()

class UserOtpForm(forms.Form):
   
    otp = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your OTP'})
    )
    captcha = ReCaptchaField()

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('user', None)
    #     super(UserOtpForm, self).__init__(*args, **kwargs)
    #     if user:
    #         self.fields['email'].initial = user.email


