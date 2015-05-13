from django import forms
from models import Ticket, TicketPost

from django.core.validators import RegexValidator

class TicketForm(forms.ModelForm):
	name = forms.CharField(required=False)
	email = forms.EmailField(required=False)
	category = forms.CharField(widget=forms.HiddenInput())
	message = forms.CharField(widget=forms.Textarea())

	class Meta:
		model = Ticket
		exclude = ['status','datetime','user','reference']

class TicketPostForm(forms.ModelForm):
	message = forms.CharField(widget=forms.Textarea())

	class Meta:
		model = TicketPost
		exclude = ['datetime','user','thread']