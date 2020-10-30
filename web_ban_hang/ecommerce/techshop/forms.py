from django import forms
from django_countries.fields import CountryField



PAYMENT_CHOICES =(
    ('S','Stripe'), 
    ('P','PayPal'),
)

class Checkoutform(forms.Form):
    street_Address =forms.CharField(widget =forms.TextInput(attrs={
        'placeholder' : 'Phuong'
    }))
    apartment_Address =forms.CharField(required =False, widget =forms.TextInput(attrs={
        'placeholder': 'Dia chi nha ....'
    }))
    country = CountryField(blank_label ='(select country)').formfield()
    zip =forms.CharField()
    same_billing_address =forms.BooleanField(widget =forms.CheckboxInput(),required =False)
    save_info = forms.BooleanField(widget =forms.CheckboxInput(),required =False)
    payment_option =forms.ChoiceField(widget =forms.RadioSelect,choices=PAYMENT_CHOICES)
 
    