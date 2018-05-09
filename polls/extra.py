from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from polls.models import Question, Choice, Scenario, Text_Input, Link, ImageScenario, ImageLink, ImageChain, BaseImage, ActionImage, Story, Authors, StoryText
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


def getTextVotes():
	with open('polls/store/stories.p', 'rb') as fp:
		stories = pickle.load(fp)
	total = 0
	votes = {}
	count = 0
	my_dict = {}
	for key in stories:
		count = count + 1
		test_stories = StoryText.objects.filter(story_id=key)
		votes = 0
		for test in test_stories:
			votes = votes + test.votes
		print('id = ' + str(key) + ', Total number of votes this story has recieved : ' + str(votes))
		size = len(stories[key])
		if size in my_dict:
			my_dict[size] = my_dict[size] + votes
		else:
			my_dict[size] = votes
		total = total + votes
	print('count = ' + str(count))
	print('total = ' + str(total))
	print(my_dict)
	x_list = []
	y_list = []
	for key in my_dict:
		x_list.append(key)
		y_list.append(my_dict[key])

	return x_list, y_list


def getAverageChains():
	# This shows us the number of image chains created by a user on average.
	users = User.objects.all()
	total = 0
	for user in users:
		chains = Authors.objects.filter(user=user)
		count = len(chains)
		print('User ' + user.username + ' has ' + str(count) + ' stories.')
		total = total + count

	average = (total/len(users))
	print('Average number of chains : ' + str(average))


def getMinMaxText():
	users = User.objects.all()
	tmin = 3000
	tmax = 0
	for user in users:
		texts = StoryText.objects.filter(user=user)
		count = len(texts)
		if count > tmax:
			tmax = count
		if count < tmin:
			tmin = count
	print('Min : ' + str(tmin))
	print('Max : ' + str(tmax))


def getMinMaxCharCount():
	texts = StoryText.objects.all()
	tmin = 10000
	tmax = 0
	total = 0
	count = len(texts)
	for text in texts:
		l = len(text.story_text)
		print('Story : ' + text.story_text)
		print('Length of story : ' + str(l))
		if l < tmin:
			tmin = l
		if l > tmax:
			tmax = l
		total = total + l

	average = total / count
	print('Min : ' + str(tmin))
	print('Max : ' + str(tmax))
	print('Average = ' + str(average))