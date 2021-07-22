from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Post
User = get_user_model()

class RegisterForm(forms.ModelForm):
    """
    The default 

    """

    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email','first_name','last_name']
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'id': 'first_name',
        })
        self.fields['last_name'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'id': 'last_name',
        })
        self.fields['email'].widget.attrs.update({
            'type': 'email',
            'class': 'form-control',
            'id': 'email',
        })    
        self.fields['password'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'id': 'password',
        })    
        self.fields['password_2'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'id': 'password2',
        })    

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data
    
    def save(self, commit=True):
            # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        if commit:
            user.save()
        return user


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text'] 
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'type': 'text',
            'class': 'form-control',
            'id': 'text',
            'name': 'text',
            'rows':'4'
        })