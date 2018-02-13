from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from polls.models import Question, Choice, Scenario, Text_Input, Link, ImageScenario, ImageLink, ImageChain, BaseImage, ActionImage, Story, Authors
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import *
import pickle
import sys


def getVotes(story):
	return story.votes


def show_stories(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	user_stories = Authors.objects.filter(user=user)
	with open('polls/store/stories.p', 'rb') as fp:
		stories = pickle.load(fp)

	# new_dict stores the stories which have been made by the user.
	new_dict = {}
	for item in user_stories:
		story = item.story
		story_id = story.id
		id_list = stories[story_id]
		image_list = []
		image_list.append(BaseImage.objects.get(id=id_list[0]))
		for i in range(1, len(id_list)):
			image_list.append(ActionImage.objects.get(id=id_list[i]))
		new_dict[story_id] = image_list

	# other_dict stores all the other stories ( the ones which this user has not created per se.)
	other_dict = {}
	for item in stories:
		if item not in new_dict:
			id_list = stories[item]
			image_list = []
			image_list.append(BaseImage.objects.get(id=id_list[0]))
			for i in range(1, len(id_list)):
				image_list.append(ActionImage.objects.get(id=id_list[i]))
			other_dict[item] = image_list

	