from django.shortcuts import render, redirect
from django.db.models import Count
from django.urls import reverse
from ..login.models import User
from .models import Poke

# Create your views here.
def index(request):
	if 'id' in request.session:
		user_pokes = Poke.objects.filter(pokee_id=request.session['id']).values('poker').annotate(num_pokes=Count('poker')).order_by('-num_pokes')

		pokes = []
		for poke in user_pokes:
			pokes.append({'poker': User.objects.get(id=poke['poker']), 'num_pokes': poke['num_pokes']})

		other_users = User.objects.exclude(id=request.session['id'])
		other_pokes = Poke.objects.exclude(pokee_id=request.session['id']).values('pokee').annotate(history=Count('pokee'))

		for poke in other_pokes:
			poke['pokee'] = User.objects.get(id=poke['pokee'])

		for user in other_pokes:
			if User.objects.get(id=user['pokee'].id):
				other_users= other_users.exclude(id=user['pokee'].id)
	else:
		return render(request, 'pokes/index.html')
	context = {
		'other_pokes' : other_pokes,
		'user_pokes': pokes,
		'other_users': other_users
	}
	return render(request, 'pokes/index.html', context)


def poke(request, id):
	Poke.objects.poke(request.session['id'], id)
	return redirect(reverse('pokes:index'))
