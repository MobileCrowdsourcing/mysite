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