from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
	for user in User.objects.all():
		print user.email

	# removes = User.objects.all().delete()
	return render(request, 'login/index.html')


def logout(request):
	request.session.flush()
	return redirect(reverse('login:index'))


def login(request):
	response = User.objects.login(**request.POST)
	if not response[0]:
		for message in response[1]:
			messages.error(request, message)
		return redirect(reverse('login:index'))

	messages.success(request, response[1])
	request.session['id'] = response[2]['id']
	request.session['first_name'] = response[2]['name']

	return redirect(reverse('pokes:index'))


def register(request):
	print request.POST
	response = User.objects.register(**request.POST)
	if not response[0]:
		for message in response[1]:
			messages.error(request, message)
		return redirect(reverse('login:index'))

	messages.success(request, response[1])

	request.session['id'] = response[2]['id']
	request.session['first_name'] = response[2]['name']
	return redirect(reverse('pokes:index'))
