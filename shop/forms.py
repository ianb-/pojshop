from django import forms
from shop.models import SaleOrder, SaleDetail

from django.core.validators import RegexValidator

class SaleOrderForm(forms.ModelForm):
	order_id = forms.CharField(widget=forms.HiddenInput(), required=False)
	user = forms.CharField(widget=forms.HiddenInput(), required=False)
	first_name = forms.CharField()
	last_name = forms.CharField()
	address1 = forms.CharField()
	address2 = forms.CharField(required=False)
	city = forms.CharField()
	county = forms.CharField()
	postcode = forms.CharField(validators=[
		RegexValidator(
			regex='^(([gG][iI][rR] {0,}0[aA]{2})|((([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y]?[0-9][0-9]?)|(([a-pr-uwyzA-PR-UWYZ][0-9][a-hjkstuwA-HJKSTUW])|([a-pr-uwyzA-PR-UWYZ][a-hk-yA-HK-Y][0-9][abehmnprv-yABEHMNPRV-Y]))) {0,}[0-9][abd-hjlnp-uw-zABD-HJLNP-UW-Z]{2}))$',
			message="Please ensure you're entering a valid UK Postcode",	
			),
		]
	)
	phone = forms.CharField(validators=[
		RegexValidator(
			regex='(0|44)(\d{4}\s(\d{6}|\d{3}\s\d{3})|\d{10})',
			message="Please ensure you're entering a valid UK telephone number"),
		])

	class Meta:
		model = SaleOrder
		fields = ['first_name','last_name','address1','address2','city','county','postcode','phone']
		exclude = ['total_price', 'shipping_price']