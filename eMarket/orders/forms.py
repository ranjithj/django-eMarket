from django import forms
from django.contrib.auth import get_user_model

from .models import UserAddress
User = get_user_model()

class GuestCheckoutForm(forms.Form):

    email = forms.EmailField()
    email2 = forms.EmailField()

    def clean_email2(self):
        email = self.cleaned_data.get("email")
        email2 = self.cleaned_data.get("email2")

        if email == email2:
            user_exists = User.objects.filter(email=email).count()

            if user_exists != 0:
                raise forms.ValidationError("User Already Exists!")
            else:
                return email2
        else:
            raise forms.ValidationError("Please check if emails are same")

class AddressForm(forms.Form):
    billing_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(addr_type="billing"),
                                             widget=forms.RadioSelect,
                                             empty_label=None,
                                             )
    shipping_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(addr_type="shipping"),
                                             widget=forms.RadioSelect,
                                             empty_label=None,
                                             )


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'street',
            'city',
            'state',
            'zipcode',
            'addr_type'
        ]