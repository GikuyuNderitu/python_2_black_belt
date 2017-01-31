from __future__ import unicode_literals
from datetime import datetime
import re
import bcrypt
from django.db import models

NAME_REGEX = re.compile(r'^[a-zA-Z\'\ ]{3,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^[a-zA-Z0-9.#!?$\+=*]{8,255}')

# Create your models here.
class UserManager(models.Manager):
	"""docstring for UserManager."""
	def login(self, **kwargs):
		errors = []
		email = str(kwargs['email'][0])
		password = str(kwargs['password'][0])
		incorrect = False

		if not EMAIL_REGEX.match(email):
			incorrect = True
			errors.append('Please insert a valid email address.')
		if not PASSWORD_REGEX.match(password):
			incorrect = True
			errors.append('Please insert a valid password.')

		if incorrect:
			return (False, errors)

		try:
			user = User.objects.get(email=email)
		except Exception as e:
			errors.append("I'm sorry, the entered email address does not exist.")
			return (False, errors)

		if user.password != bcrypt.hashpw(password, user.password.encode()):
			errors.append('I\'m sorry, the password you entered was wrong.')
			return (False, errors)

		return (True, 'Successful Login', {'id': user.id, 'name' : user.name})




	def register(self, **kwargs):
		errors = []
		name = str(kwargs['name'][0])
		alias = str(kwargs['alias'][0])
		email = str(kwargs['email'][0])
		password = str(kwargs['password'][0])
		confirm = str(kwargs['confirmation'][0])
		incorrect = False

		# Name check
		if not NAME_REGEX.match(name):
			incorrect = True
			errors.append("Please enter a name with only characters and is at least 3 characters long.")


		# Email Check
		if not EMAIL_REGEX.match(email):
			incorrect = True
			errors.append("Please enter a valid email address.")

		# Password Checks
		if not PASSWORD_REGEX.match(password):
			incorrect = True
			errors.append("Please enter a password with 8 or more characters and with valid characters\n [Valid characters are: '.' '#' '!' '?' '+' '=' '*'] ")
		elif not password == confirm:
			incorrect = True
			errors.append("Passwords do not match, try again")

		# DOB Checks
		# Collect error prone values from kwargs and validate
		try:
			dob = datetime.strptime(str(kwargs['dob'][0]), '%d %B, %Y')
		except Exception as e:
			incorrect = True
			errors.append("Please enter a value for 'Date of Birth'")

		try:
			delta = datetime.now() - dob
			if delta.days <= 0:
				incorrect = True
				errors.append("I'm sorry, you may only select any day prior to today")
		except Exception as e:
			pass

		# Check to see if flag was tripped at all
		if incorrect:
			return (False, errors)

		hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))

		try:
			user = User.objects.create(name=name, password=hashed, email=email, alias=alias, d_o_B=dob)
		except Exception as e:
			errors.append("I'm sorry, there is already a user with that email.")
			return (False, errors)

		return (True, 'Successfully registered!', {'id' : user.id, 'name' : name})


class User(models.Model):
	"""docstring for User."""
	name = models.CharField(max_length=90)
	alias = models.CharField(max_length=90, blank=True)
	password = models.CharField(max_length=255)
	email = models.CharField(max_length=255, unique=True)
	d_o_B = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
