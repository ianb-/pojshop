from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
	reference = models.CharField(max_length=24)
	user = models.ForeignKey(User, null=True, blank=True)
	name = models.CharField(max_length=32)
	email = models.EmailField(max_length=64)
	status = models.CharField(max_length=6, default="Open")
	order_id = models.CharField(max_length=24, blank=True, null=True)
	category = models.CharField(max_length=32,
		choices=(
			('general','General Inquiry'),
			('returns', 'Returns'),
			('support', 'Support Query'),
		)
	)
	datetime = models.DateTimeField(auto_now_add=True)
	message = models.TextField()

	def __unicode__(self):
		return self.reference

class TicketPost(models.Model):
	thread = models.ForeignKey(Ticket)
	user = models.ForeignKey(User)
	datetime = models.DateTimeField(auto_now_add=True)
	message = models.TextField()

	def __unicode__(self):
		return self.thread + ' - ' + self.user.username