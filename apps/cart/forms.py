from django import forms

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={"class": "qty-input", "style": "width: 80px;"})
    )

class CheckoutForm(forms.Form):
    address      = forms.CharField(max_length=255)
    city         = forms.CharField(max_length=100)
    postal_code  = forms.CharField(max_length=20)
    payment_method = forms.ChoiceField(
        choices=[("card", "Tarjeta"), ("paypal", "PayPal")]
    )
