from __future__ import unicode_literals
from ..login.models import User
from django.db import models

# Create your models here.
class PokeManager(models.Manager):
	"""docstring for PokeManager."""
	def poke(self, poker, pokee):
		Poke.objects.create(poker_id=poker, pokee_id=pokee)
		return False

class Poke(models.Model):
	"""docstring for Poke."""
	poker = models.ForeignKey(User, related_name='initiator')
	pokee = models.ForeignKey(User, related_name='initiated')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = PokeManager()
