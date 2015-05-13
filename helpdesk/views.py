from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from models import Ticket, TicketPost
from forms import TicketForm, TicketPostForm
import random

def new_id():
	x = ''.join(random.choice('0123456789ABCDEF') for i  in range(4))
	y = ''.join(random.choice('0123456789ABCDEF') for i  in range(4))
	z = x + '-' + y
	try:
		t = Ticket.objects.get(reference=z)
	except Ticket.DoesNotExist:
		return z
	return new_id()

def staff_check(user):
	return user.is_staff

def contact(request):
	data = {}
	if request.method == 'POST':
		form = TicketForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.reference = new_id()
			if request.user.is_authenticated():
				f.user = request.user
				f.save()
			else:
				form.save()
			return redirect('shop:frontpage')
		else:
			data['form'] = form
			return render(request, 'helpdesk/contact.html', data)
	else:
		data['form'] = TicketForm()
		return render(request, 'helpdesk/contact.html', data)

def ticket(request, ref):
	data = {}
	try:
		t = Ticket.objects.get(reference=ref)
	except Ticket.DoesNotExist:
		raise Http404("Ticket does not exist")
	if request.user != t.user and not request.user.is_staff:
		raise Http404("Access denied")
	if request.method == 'POST':
		form = TicketPostForm(request.POST)
		if form.is_valid():
			f = form.save(commit=False)
			f.user = request.user
			f.thread = t
			f.save()
			return redirect('helpdesk:ticket', t.reference)
		else:
			print form.errors
	data['ticket'] = t
	data['replies'] = TicketPost.objects.filter(thread=t)
	return render(request, 'helpdesk/ticket.html', data)

@user_passes_test(staff_check, login_url='/accounts/login/')
def change_ticket_status(request, ref):
	try:
		ticket = Ticket.objects.get(reference=ref)
	except:
		return HttpResponse("Something went wrong... That's all the help I can give you right now")
	state = ticket.status
	if state == "Open":
		ticket.status = "Closed"
	else:
		ticket.status = "Open"
	ticket.save()
	return redirect('helpdesk:ticket', ref)

@user_passes_test(staff_check, login_url='/accounts/login/')
def delete_ticket(request, ref):
	try:
		ticket = Ticket.objects.get(reference=ref)
	except:
		return HttpResponse("Can't find the ticket. Well, you were trying to delete it...")
	ticket.delete()
	return redirect('cpanel:dashboard')