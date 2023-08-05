from django import forms
from .models import UserBase
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)


# Password Reset Confirm Form
class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "New Password",
                "id": "form-newpass",
            }
        ),
    )

    new_password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Repeat Password",
                "id": "form-newpass2",
            }
        ),
    )


# Password Reset Form
class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "form-email",
            },
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "The given email does not have a account registered with it",
            )
        return email


# User Edit Form
class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Account email",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "form-email",
                "readonly": "True",
            }
        ),
    )
    first_name = forms.CharField(
        label="First Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "First Name",
                "id": "form-firstname",
            }
        ),
    )
    last_name = forms.CharField(
        label="Last Name",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Last Name",
                "id": "form-lastname",
            }
        ),
    )
    phone_number = forms.CharField(
        label="Phone Number",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Phone Number",
                "id": "form-phone_number",
            }
        ),
    )

    address = forms.CharField(
        label="Address",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Address",
                "id": "form-address",
            }
        ),
    )

    town_city = forms.CharField(
        label="City/Town",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "City/Town",
                "id": "form-city",
            }
        ),
    )

    state = forms.CharField(
        label="State",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "State",
                "id": "form-state",
            }
        ),
    )

    postcode = forms.CharField(
        label="Post Code",
        max_length=12,
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Post Code",
                "id": "form-postcode",
            }
        ),
    )

    

    class Meta:
        model = UserBase
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "town_city",
            "state",
            "postcode",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
        self.fields["email"].required = True


# Registration Form
class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label="Enter Username", min_length=4, max_length=50, help_text="Required"
    )
    email = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
    )
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = (
            "user_name",
            "email",
        )

    def clean_username(self):
        user_name = self.cleaned_data["user_name"].lower()
        r = UserBase.objects.filter(user_name=user_name)
        # checks of the username alreasy exists in the database
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Please use another email, this is already taken"
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Username"}
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control mb-3",
                "placeholder": "E-mail",
                "name": "email",
                "id": "id_email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Repeat Password"}
        )


class UserLoginForm(forms.Form):
    username = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-3",
                "placeholder": "Email",
                "id": "login-user",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )
