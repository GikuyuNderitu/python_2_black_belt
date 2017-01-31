from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.
def index(request):
	return redirect(reverse('login:index'))
