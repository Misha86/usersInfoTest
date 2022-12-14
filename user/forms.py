"""Module with forms for api application."""
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser


class UploadFileForm(forms.Form):
    """Class form for uploading .cvs and .xml files."""

    file_csv = forms.FileField(widget=forms.FileInput(attrs={'accept': '.csv'}))
    file_xml = forms.FileField(widget=forms.FileInput(attrs={'accept': '.xml'}))


class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users.

    Includes all the required fields, plus a repeated password.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        """Metaclass where CustomUser model and fields are specified."""

        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'avatar']

    def clean_password2(self):
        """Check that the two password entries match."""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(forms.ModelForm):
    """A form for updating users.

    Includes all the fields on the user, but replaces the password field with
    admin"s disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        """Metaclass for specifying CustomUser model and its fields."""

        model = CustomUser
        fields = ('username', 'password', 'first_name', 'last_name')
