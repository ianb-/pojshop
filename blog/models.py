from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify

class Article(models.Model):
	title = models.CharField(max_length=128)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User)
	slug = models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Article, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title