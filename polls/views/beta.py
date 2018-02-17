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
	base = BaseImage.objects.all()
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
			'base':base
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
	if 'action_list' in request.session:
		del request.session['action_list']
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
	base_image = BaseImage.objects.get(id=base_id)
	stories = Story.objects.filter(base_image=base_image)
	print('Base id ' + str(base_id))
	base_id = int(base_id)
	print(type(base_id))
	new_dict = {}
	fp = open('polls/store/stories.p', 'rb')
	print(fp)
	all_dict = pickle.load(fp)
	fp.close()
	for story in stories:
		story_list = all_dict[story.id]
		new_list = []
		new_list.append(base_image)
		count = 0
		for item in story_list:
			if count == 0:
				count = count + 1
				continue
			image = ActionImage.objects.get(id=item)
			new_list.append(image)
			count = count + 1


		new_dict[story.id] = new_list
	request.session['base_id'] = base_image.id
	request.session.modified=True
	return render(request, 'polls/select_story.html', {
		'user': user,
		'new_dict': new_dict,
		'user_log': request.user.is_authenticated,
		'base_image': base_image,
		})


def story_redirect(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	story_id = int(request.POST['story_id'])
	return HttpResponseRedirect(reverse('polls:add_action', args=[story_id]))


def add_action(request, story_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	print("BASE ID showing")
	user = request.user
	story_id = int(story_id)

	# story_id = int(request.POST['story_id'])
	print('Story ID passed : ' + str(story_id))
	if story_id == 0:
		# User has not chosed a chain, but the base image.
		print('Base image chosen.')
		story = None
	else:
		print('Chain Chosen')
		# Unpickle and load a list with the story
		fp = open('polls/store/stories.p', 'rb')
		stories = pickle.load(fp)
		id_story = stories[story_id]
		story = []
		story.append(BaseImage.objects.get(id=id_story[0]))
		for i in range(1, len(id_story)):
			story.append(ActionImage.objects.get(id=id_story[i]))
		fp.close()
	if 'base_id' not in request.session:
		print('No Base ID XD')
	else:
		print('Base id : ' + str(request.session['base_id']))
	action_images = ActionImage.objects.all()
	base_id = int(request.session['base_id'])
	base_image = BaseImage.objects.get(id=base_id)
	if 'action_list' not in request.session:
		# User has not added any actions yet.
		action_image_list = None
	else:
		action_list = request.session['action_list']
		action_image_list = []
		for action_id in action_list:
			action_image_list.append(ActionImage.objects.get(id=action_id))
	return render(request, 'polls/add_action.html', {
		'user': user,
		'story': story,
		'action_images': action_images,
		'story_id': story_id,
		'base_image': base_image,
		'user_log': user.is_authenticated,
		'action_list': action_image_list,
		})


def continue_story(request, story_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	user = request.user
	if 'action_list' in request.session:
		action_list = request.session['action_list']
		del request.session['action_list']
	else:
		action_list = []


	story_id = int(story_id)
	base_id = request.session['base_id']
	base_id = int(base_id)
	base_image = BaseImage.objects.get(id=base_id)
	print('Story ID : ' + str(story_id) + ', base_id : ' + str(base_id))
	with open('polls/store/stories.p', 'rb') as fp:
			stories = pickle.load(fp)
	if story_id == 0:
		# User is adding directly to a base image.
		print('Add directly to Base.')
		new_story = [base_id]
	else:
		# User is adding to a chain
		print('Adding to a current story.')
		story = stories[story_id]
		new_story = []
		for image in story:
			new_story.append(image)
	
	for image_id in action_list:
		new_story.append(int(image_id))
	last_action_image=ActionImage.objects.get(id=action_list[len(action_list)-1])
	check_stories = Story.objects.filter(base_image=base_image, last_action_image=last_action_image)
	found = False
	for tup in check_stories:
		tup_id = tup.id
		check_list = stories[tup_id]

		if len(new_story) != len(check_list):
			# Not the same list
			continue
		found = True
		for i in range(0, len(new_story)):
			if new_story[i] != check_list[i]:
				flag = False
				break
		if found is True:
			# Same story found.
			story = Story.objects.get(id=tup.id)
			print('Story id found : ' + str(tup.id))
			story.votes = story.votes + 1
			story.save()
			check = Authors.objects.filter(story=story, user=user)
			print(check)
			if check is None or len(check) == 0:
				author = Authors(story=story, user=user)
				author.save()
			break

	if found is False:
		# No story found
		story = Story(base_image=base_image, last_action_image=last_action_image, votes=0)
		story.save()
		author = Authors(story=story, user=user)
		author.save()
		print("Created a new story with ID : " + str(story.id))
		stories[story.id] = new_story
		with open('polls/store/stories.p', 'wb') as fp:
			pickle.dump(stories, fp)

	print('Success !')
	return HttpResponseRedirect(reverse('polls:continue_success', args=[story.id]))


def continue_success(request, story_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	return render(request, 'polls/thank_you.html', {
		'user_log': request.user.is_authenticated,
		'story_id': story_id,
		})


def add_success(request, story_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	if request.method != 'POST':
		print("GET attempted at add_success.")
		raise Http404("Page not Found.")

	story_id = int(story_id)
	print('story_id = ' + str(story_id))
	action_image_id = request.POST['action_image_id']
	print('Action Image ID : ' + action_image_id)
	action_image_id = int(action_image_id)
	if 'action_list' in request.session:
		request.session['action_list'].append(action_image_id)
	else:
		new_action_list = [action_image_id]
		request.session['action_list'] = new_action_list
	request.session.modified=True

	return render(request, 'polls/ask_redirect.html', {
		'user': request.user,
		'user_log': request.user.is_authenticated,
		'story_id': story_id,
		'action_image_id': action_image_id,
		})