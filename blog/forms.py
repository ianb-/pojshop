from django import forms
from blog.models import Article
from datetime import datetime

class ArticleForm(forms.ModelForm):
	title = forms.CharField(max_length=128)
	content = forms.CharField(widget=forms.Textarea())
	created = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Article
		fields = ('title','content',)