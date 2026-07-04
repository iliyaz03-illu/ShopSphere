from django import forms


class ShippingForm(forms.Form):

    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "checkout-input",
            "placeholder": "Full Name"
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "class": "checkout-input",
            "placeholder": "Phone Number"
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "checkout-input",
            "rows": 3,
            "placeholder": "Address"
        })
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "checkout-input",
            "placeholder": "City"
        })
    )

    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "checkout-input",
            "placeholder": "State"
        })
    )

    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "checkout-input",
            "placeholder": "Pincode"
        })
    )