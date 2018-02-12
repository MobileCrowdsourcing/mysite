from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from polls.models import Question, Choice, Scenario, Text_Input, Link, ImageScenario, ImageLink, ImageChain, BaseImage, ActionImage
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import *
import pickle
import sys


# Making the chain and redirecting
def add_story(request, first_image_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	to_image_id = request.GET['image_id']

	if first_image_id is None:
		print('First image not found')
		raise Http404('Page Not Found')

	print('First Image ID : ' + str(first_image_id) + ', Second Image ID : ' + str(to_image_id))
	start_image = ImageScenario.objects.get(id=first_image_id)
	end_image = ImageScenario.objects.get(id=to_image_id)

	new_chain = ImageChain(start_image=start_image, end_image=end_image, votes=0)
	new_chain.save()
	new_list = [first_image_id, to_image_id]

	print('New Chain ID : ' + str(new_chain.id))
	try:
		fp = open('polls/store/gs.p', 'rb')
	except:
		print('Error : ' + str(sys.exc_info()[0]))
		raise Http404('Cannot Access DB')

	dgraph = pickle.load(fp)
	dgraph[new_chain.id] = new_list
	fp.close()

	try:
		fp = open('polls/store/gs.p', 'wb')
		pickle.dump(dgraph, fp)
		fp.close()
	except:
		print('Error : ' + str(sys.exc_info()[0]))
		raise Http404('Cannot Access DB')

	print('Sending new_chain_id : ' + str(new_chain.id))
	chain_id = new_chain.id
	return HttpResponseRedirect(reverse('polls:choose_2image', args=[chain_id]))


def add_base(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	if request.method == "POST":
		url = request.POST['url']
		text = request.POST['imageText']
		new_image = BaseImage(user=user, url=url, text=text)
		new_image.save()
		print("New BaseImage Added")
		return HttpResponseRedirect(reverse('home'))
	else:
		return render(request, 'polls/add_base.html', {
			'user': user,
			'user_log': request.user.is_authenticated,
			})


def make_sequence(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	# Showing list of starting images to user here.
	images = BaseImage.objects.all()
	return render(request, 'polls/make_sequence.html', {
		'user': user,
		'images': images,
		'user_log': request.user.is_authenticated,
		})


def select_story(request, base_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	