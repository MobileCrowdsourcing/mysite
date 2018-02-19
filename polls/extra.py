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


def getStory(story_id):
	with open('polls/store/stories.p', 'rb') as fp:
		stories = pickle.load(fp)

	id_list = stories[story_id]
	image_list = []
	image_list.append(BaseImage.objects.get(id=id_list[0]))
	for i in range(1, len(id_list)):
		image_list.append(ActionImage.objects.get(id=id_list[i]))

	return image_list


def getVotes():
	with open('polls/store/stories.p', 'rb') as fp:
		stories = pickle.load(fp)

	my_dict = {}
	for key in stories:
		size = len(stories[key])
		temp = Story.objects.get(id=int(key)).votes
		print('temp = ' + str(temp))
		votes = temp + 1
		if size in my_dict:
			my_dict[size] = my_dict[size] + votes
		else:
			my_dict[size] = votes

	id_list = []
	vote_list = []
	for key in my_dict:
		id_list.append(key)
		vote_list.append(my_dict[key])

	return id_list, vote_list

def getPlot():
	with open('polls/store/stories.p', 'rb') as fp:
		stories = pickle.load(fp)

	print(stories)
	plot = {}
	for key in stories:
		image_list = stories[key]
		size = len(image_list)
		if size in plot:
			plot[size] = plot[size] + 1
		else:
			plot[size] = 1

	size_list = []
	count_list = []
	for key in plot:
		size_list.append(key)
		count_list.append(plot[key])

	return size_list, count_list