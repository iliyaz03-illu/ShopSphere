from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            "image",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
        ]

        widgets = {

            "address": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter your address"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "placeholder": "Phone Number"
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "placeholder": "City"
                }
            ),

            "state": forms.TextInput(
                attrs={
                    "placeholder": "State"
                }
            ),

            "pincode": forms.TextInput(
                attrs={
                    "placeholder": "Pincode"
                }
            ),

        }