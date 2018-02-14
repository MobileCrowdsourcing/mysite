from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from polls.models import Question, Choice, Scenario, Text_Input, Link, ImageScenario, ImageLink, ImageChain, BaseImage, ActionImage, Story, Authors
from polls.models import StoryText
from polls.extra import getStory
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from random import *
import pickle
import sys
from random import shuffle


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
	u_stories = Authors.objects.filter(user=user)
	with open('polls/store/stories.p', 'rb') as fp:
		stories = pickle.load(fp)

	# new_dict stores the stories which have been made by the user.
	user_stories = []
	for item in u_stories:
		user_stories.append(item)
	shuffle(user_stories)
	new_list = []
	new_dict = {}
	for item in user_stories:
		story = item.story
		story_id = story.id
		new_list.append(story_id)
		id_list = stories[story_id]
		image_list = []
		image_list.append(BaseImage.objects.get(id=id_list[0]))
		for i in range(1, len(id_list)):
			image_list.append(ActionImage.objects.get(id=id_list[i]))
		new_dict[story_id] = image_list

	# other_dict stores all the other stories ( the ones which this user has not created per se.)
	print('Stories : ')
	print(stories)
	other_dict = {}
	for item in stories:
		if item not in new_dict:
			id_list = stories[item]
			print('id_list type = ' + str(type(id_list)))
			image_list = []
			image_list.append(BaseImage.objects.get(id=id_list[0]))
			for i in range(1, len(id_list)):
				image_list.append(ActionImage.objects.get(id=id_list[i]))
			other_dict[item] = image_list


	story_tuples = Story.objects.order_by('votes')
	lim = len(story_tuples)
	i = lim - 1
	count = 0
	popular_stories = []
	while count < 3:
		count = count + 1
		popular_stories.append(story_tuples[i])
		i = i - 1

	# pop_dict will store the three most popular stories in the database.
	pop_dict = {}
	for popS in popular_stories:
		id_list = stories[popS.id]
		image_list = []
		image_list.append(BaseImage.objects.get(id=id_list[0]))
		for i in range(1, len(id_list)):
			image_list.append(ActionImage.objects.get(id=id_list[i]))
		pop_dict[popS.id] = image_list

	#Passing all this to the user.
	return render(request, 'polls/show_stories.html', {
		'user': request.user,
		'user_log': request.user.is_authenticated,
		'new_dict': new_dict,
		'other_dict': other_dict,
		'pop_dict': pop_dict,
		'new_list': new_list,
		})


def work_story(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	if request.method != 'POST':
		raise Http404('Invalid Access, Page not found.')

	story_id = request.POST['story_id']
	story = Story.objects.get(id=story_id)
	check = Authors.objects.filter(user=user, story=story)
	if len(check) == 0:
		# User is not an author.
		# We cannot allow editing access.
		return HttpResponseRedirect(reverse('polls:read_stories', args=[story_id]))
	else:
		# User is an author.
		# Allow editing Access.
		return HttpResponseRedirect(reverse('polls:write_story', args=[story_id]))


def read_stories(request, story_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	if story_id == None:
		print('story_id is None, please check.')
		raise Http404('Page Not Found')
	story_id = int(story_id)
	story = Story.objects.get(id=story_id)
	if request.method == "GET":
		st_dict = {}
		image_list = getStory(story_id)
		# All story texts written for this story.
		storyTexts = StoryText.objects.filter(story=story)
		if len(storyTexts) == 0:
			storyTexts = None
		return render(request, 'polls/read_stories.html', {
			'user': user,
			'user_log': user.is_authenticated,
			'storyTexts': storyTexts,
			'story_id': story_id,
			'image_list': image_list,
			})
	else:
		story_text_id = int(request.POST['story_text_id'])
		print('Story Text ID : ' + str(story_text_id))
		storytext = StoryText.objects.get(id=story_text_id)
		storytext.votes = storytext.votes + 1
		storytext.save()
		print('Voted for this story. Check admin site.')
		return HttpResponseRedirect(reverse('polls:show_stories'))


def write_story(request, story_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	if story_id == None:
		print('Story ID none, please check.')
		raise Http404('Page not found')

	if request.method == "GET":
		story_id = int(story_id)
		story = Story.objects.get(id=story_id)
		storyTexts = StoryText.objects.filter(story=story)
		image_list = getStory(story_id)
		check = StoryText.objects.filter(story=story, user=user)
		if len(check) == 0:
			# User has not written a story yet.
			user_text = None
		else:
			user_text = check[0].story_text
		if len(storyTexts) == 0:
			storyTexts = None
		return render(request, 'polls/write_story.html', {
			'user': user,
			'user_log': user.is_authenticated,
			'storyTexts': storyTexts,
			'story_id': story_id,
			'image_list': image_list,
			'user_text': user_text,
			})
	else:
		story_id = int(story_id)
		story_text = request.POST['story_text_input']
		story = Story.objects.get(id=story_id)
		print("User has given some input for this story. Adding it to db.")
		check = StoryText.objects.filter(user=user, story=story)
		if len(check) == 0:
			# User has never written for this story before.
			new_story_text = StoryText(user=user, story=story, story_text=story_text, votes=0)
			new_story_text.save()
			print("New Story Text Added. ID : " + str(new_story_text.id) + ", text : " + str(new_story_text.story_text))
			return HttpResponseRedirect(reverse('polls:show_stories'))
		else:
			# User has alraedy written some text for this story.
			old_story_text = check[0]
			old_story_text.story_text = story_text
			old_story_text.save()
			print("Adding to already existing story.")
			return HttpResponseRedirect(reverse('polls:show_stories'))


def add_action_image(request, story_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	if request.method != 'POST':
		print('User trying GET, please check')
		raise Http404('Page not Found')

	action_url = request.POST['url']
	print('Action URL : ' + action_url)
	action_image = ActionImage(url=action_url)
	action_image.save()
	print("New Action Image Added")
	return HttpResponseRedirect(reverse('polls:add_action', args=[int(story_id)]))
