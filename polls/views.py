from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from .models import Question, Choice, Scenario, Text_Input, Link, ImageScenario, ImageLink, ImageChain
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from random import *
import pickle
import sys
# class IndexView(generic.ListView):
# 	template_name = 'polls/index.html'
# 	context_object_name = 'latest_q_list'

# 	def get_queryset(self):
# 		# Returning the last five asked questions
# 		# return Question.objects.order_by('-pub_date')[:5]
# 		return Question.objects.filter(
# 			pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/details.html'

	def get_queryset(self):
		return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# @login_required
def index(request):
	print('Hello')
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	latest_q_list = Question.objects.order_by('-pub_date')[:5]
	template = loader.get_template('polls/index.html')
	context = {
		'latest_q_list': latest_q_list
	}
	# output = "; ".join([q.question_text for q in latest_q_list])
	return render(request, 'polls/index.html', {'latest_q_list' : latest_q_list, 'user_log' : request.user.is_authenticated})
	# return HttpResponse(template.render(context, request))
    # return HttpResponse("Hello, world. You're at the polls index.")


# home page
def home_page(request):
	return render(request, 'polls/home.html', {
		'user_log': request.user.is_authenticated,
		})


def login_user(request):

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('home'))
		else:
			return render(request, 'polls/login.html', {
				'error_message' : 'Username / Password incorrect'
				})
	else:
		if(request.session.has_key('error_m')):
			error_m = request.session['error_m']
			del request.session['error_m']
			request.session.modified = True
			return render(request, 'polls/login.html', {
				'error_message' : error_m
				})
		return render(request, 'polls/login.html')


def logout_user(request):

	print('Logging out User ' + str(request.user.username))
	logout(request)
	return HttpResponseRedirect(reverse('login_user'))


def pengu(request):
	return HttpResponseRedirect("http://www.youtube.com")


def detail(request, question_id):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	try:
		question = Question.objects.get(id=question_id)
	except Question.DoesNotExist:
		raise Http404("This Question does not exist.")
	return render(request, 'polls/details.html', {'question' : question, 'user_log': request.user.is_authenticated})

    # return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	try:
		question = Question.objects.get(id=question_id)
	except Question.DoesNotExist:
		raise Http404(" Question does not exist. ")

	return render(request, 'polls/results.html', {'question' : question, 'user_log': request.user.is_authenticated })
    # return HttpResponse(response % question_id)


def vote(request, question_id):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	try:
		question = Question.objects.get(id=question_id)
	except Question.DoesNotExist:
		raise Http404(" Question does not exist. ")
	try:
		s_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/details.html', {
			'question' : question,
			'error_message' : 'You did not make a choice.',
			'user_log': request.user.is_authenticated
			})
	else:
		s_choice.votes += 1
		s_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    # return HttpResponse("You're voting on question %s." % question_id)


def narration(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	print('Taking input about a question now')

	scenario_list = Scenario.objects.order_by('id')
	return render(request, 'polls/scenarios.html', {
		'sc_list': scenario_list,
		'user_log': request.user.is_authenticated
		})
	# return('Hello')


def make_scenario(request, sc_id):

	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	scenario = Scenario.objects.get(id=sc_id)
	path_list = scenario.text_input_set.all()

	return render(request, 'polls/make_scenario.html', {
		'path_list': path_list,
		'user_log': request.user.is_authenticated,
		'scenario': scenario
		})
	# return HttpResponse('You are making a story on scenario ' + str(sc_id))


def create_path(request, sc_id):

	scenario = Scenario.objects.get(id=sc_id)
	print('Working on scenario : ' + str(scenario))

	if request.method != 'POST':
		raise Http404("This page does not Exist")
	else:
		text = request.POST['path']
		scenario.text_input_set.create(input_text=text)
		print('New path created : ' + str(text))
		scenario.save()
		return HttpResponseRedirect(reverse('polls:scenarios'))


def pathInput(request, text_input_id):

	path = Text_Input.objects.get(id=text_input_id)


def make_scenario_link(request, flag=0, sc_id=None, path_id=None, sc_t_id=None):

	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	print('Flag = ' + str(flag))
	if flag == '0':
		# Showing scenarios to start from
		print("Choosing scenario..")
		sc_list = Scenario.objects.all()
		return render(request, 'polls/make_link.html', 
			{
			'user_log': request.user.is_authenticated,
			'sc_list': sc_list
			})
	elif flag == '1':
		# Displaying the list of paths for this scenario (sc_id)
		if sc_id is None:
			raise Http404('Not Found.')

		s = Scenario.objects.get(id=sc_id)
		path_list = s.text_input_set.all()
		return render(request, 'polls/choose_path.html',
			{
			'user_log': request.user.is_authenticated,
			'path_list': path_list,
			'scenario': s
			})
	elif flag == '2':
		# Choose scenario to go to.
		s = Scenario.objects.exclude(id=sc_id)
		sc_f = Scenario.objects.get(id=sc_id)
		path = Text_Input.objects.get(id=path_id)
		return render(request, 'polls/choose_dest.html', 
			{
			'user_log': request.user.is_authenticated,
			'sc_list': s,
			'path': path,
			'sc_f': sc_f
			})
	else:
		sc_f = Scenario.objects.get(id=sc_id)
		sc_t = Scenario.objects.get(id=sc_t_id)
		path = Text_Input.objects.get(id=path_id)

		print('Path created successfully')
		link = Link(scenario_from=sc_f, scenario_to=sc_t, link_path=path, popularity=1)
		link.save()
		return HttpResponseRedirect(reverse('polls:index'))


def link_images(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	if request.method == 'GET':
		images = ImageScenario.objects.all()
		image_count = len(images)
		pos1 = randint(0, image_count-1)

		image1 = images[pos1]
		pos2 = pos1
		while(pos1 == pos2):
			pos2 = randint(0, image_count-1)

		image2 = images[pos2]

		# We have two images, stored in image1 and image2
		# We now present them to the user and ask them to say if these two images can be linked together somehow

		# We first check if an entry exists in our database with link from image1 to image2
		links = ImageLink.objects.all()
		im_link = None
		for link in links:
			if(link.image_from == image1 and link.image_to == image2):
				im_link = link
				break

		if im_link == None:
			im_link = ImageLink(image_from=image1, image_to=image2)

		im_link.save()
		return HttpResponseRedirect(reverse('polls:vote_link', args=(im_link.id,)))
	else:
		# For POST method
		raise Http404("This page does not Exist")


def vote_link(request, im_link_id):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	try:
		im_link = ImageLink.objects.get(id=im_link_id)
	except:
		raise Http404('Page Not Found')
	# if im_link is None:
	print('Link obtained : ' + str(im_link.id))
	return render(request, 'polls/link_image.html', {
		'im_link': im_link,
		'user_log': request.user.is_authenticated
		})
	

def update_link(request, link_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	if request.method != 'POST':
		raise Http404("This page does not Exist")
	print('Updating link ID : ' + str(link_id))
	im_link = ImageLink.objects.get(id=link_id)
	if request.POST['choice'] == 'yes':
		print('User has voted yes for this link.')
		im_link.vote = im_link.vote+1
	else:
		if request.POST['choice'] == 'no':
			print('User has voted no for this link')
			im_link.vote = im_link.vote-1
	im_link.save()
	return HttpResponseRedirect(reverse('polls:view_image_links'))


def getVote(link):
	try:
		v = link.vote
	except:
		v = link.votes
	return v


def view_image_links(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	links = ImageLink.objects.all()
	my_list = []
	for link in links:
		my_list.append(link)


	sorted_list = sorted(my_list, key=getVote, reverse=True)

	return render(request, 'polls/view_links.html', {
		'user_log': request.user.is_authenticated,
		'im_list': sorted_list[:15]
		})


def image_grid(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	if request.method=='GET':
		from_list = ImageScenario.objects.all()
		to_list = ImageScenario.objects.all()

		return render(request, 'polls/image_grid.html', {
			'user_log': request.user.is_authenticated,
			'from_list': from_list,
			'to_list': to_list
			})


def show_chains(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	try:
		fp = open('polls/store/gs.p', 'rb')
	except:
		print('Error : ' + str(sys.exc_info()[0]))
		raise Http404('Page Not Found')

	dgraph = pickle.load(fp)
	fp.close()
	new_dict = {}
	for item in dgraph:
		id_list = dgraph[item]
		new_list = []
		for i in id_list:
			new_list.append(ImageScenario.objects.get(id=i))
		new_dict[item]=new_list
	print('Showing all chains to user.')
	return render(request, 'polls/select_chain.html', {
		'user_log': request.user.is_authenticated,
		'chains': new_dict,
		})


def choose_image(request, chain_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))
	try:
		fp = open('polls/store/gs.p', 'rb')
	except:
		print('Error : ' + str(sys.exc_info()[0]))
		raise Http404('Page Not Found')
	# print('chain_id : ' + str(chain_id))
	if chain_id is None:
		try:
			chain_id = int(request.GET['chain_id'])
		except:
			if chain_id is None:
				print('Error : ' + str(sys.exc_info()[0]))
				raise(Http404('Bad Request from previous Page'))

	print(str(chain_id) + ', ' + str(type(chain_id)))
	images = ImageScenario.objects.all()
	dgraph = pickle.load(fp)
	fp.close()
	return render(request, 'polls/choose_image.html', {
		'user_log': request.user.is_authenticated,
		'images': images,
		'chain_id': chain_id,
		})


def check_chain(request, chain_id=None):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	if request.method != 'POST':
		raise Http404("This page does not Exist")
	image_id = int(request.POST['image_id'])
	print('Selected Image ID : ' + str(image_id))
	try:
		fp = open('polls/store/gs.p', 'rb')
	except:
		print('Error : ' + str(sys.exc_info()[0]))
		raise Http404('Page Not Found')
	print('chain_id : ' + chain_id)
	chain_id = int(chain_id)
	dgraph = pickle.load(fp)
	fp.close()
	start_image_id = dgraph[chain_id][0]
	to_image_id = image_id
	start_image = ImageScenario.objects.get(id=start_image_id)
	to_image = ImageScenario.objects.get(id=to_image_id)

	current_chain = dgraph[chain_id]
	s_chain = []
	for item in current_chain:
		s_chain.append(item)
	s_chain.append(to_image_id)
	# s_chain = current_chain.append(to_image_id)
	length = len(s_chain)
	links1 = ImageChain.objects.filter(start_image=start_image, end_image=to_image)
	flag = False
	for link in links1:
		chain = dgraph[link.id]
		if(len(chain) != length):
			continue
		flag = True
		for i in range(0, length):
			if(chain[i] != s_chain[i]):
				flag = False
		if(flag is True):
			break
	print('Flag = ' + str(flag))
	if(flag is True):
		# Chain exists
		print('Flag is true.')
		ch = ImageChain.objects.get(id=link.id)
		ch.votes = ch.votes + 1
		ch.save()
		new_chain_id = link.id
	else:
		# We have to add a new chain, and a new row in the table
		# new chain -> s_chain
		print('Flag is False.')
		new_chain = ImageChain(start_image=start_image, end_image=to_image, votes=0)
		new_chain.save()
		new_chain_id = new_chain.id
		print('Old dgraph :')
		print(dgraph)
		dgraph[new_chain.id] = s_chain
		print('New dgraph :')
		print(dgraph)
		try:
			fp = open('polls/store/gs.p', 'wb')
		except:
			print('Error : ' + str(sys.exc_info()[0]))
			raise Http404('Page Not Found')
		pickle.dump(dgraph, fp)
		fp.close()
	# s_chain is the new chain (current chain for the next page)
	# Send s_chain back to the same url
	print('Sending new_chain_id : ' + str(new_chain_id))
	chain_id = new_chain_id
	return HttpResponseRedirect(reverse('polls:choose_2image', args=[chain_id]))
	# return render(request, 'polls/make_image_chain.html', {
	# 	'user_log' : request.user.is_authenticated,
	# 	})


# function to start building new chains
def start_story(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	# All images
	images = ImageScenario.objects.all()

	return render(request, 'polls/start_story.html', {
		'user_log': request.user.is_authenticated,
		'images': images,
		})


# function to choose the second image
def start_story_2(request):
	if request.user.is_authenticated:
		print("Logged in as " + str(request.user.username))
	else:
		print("Redirecting..")
		request.session['error_m'] = 'Please Login First'
		request.session.modified = True
		return HttpResponseRedirect(reverse('login_user'))

	# Choosing the second image.
	# ID of first image
	image1_id = request.GET['image_id']
	# First Image
	image1 = ImageScenario.objects.get(id=image1_id)
	all_images = ImageScenario.objects.all()
	# images = ImageScenario.objects.filter(id!=image1_id)
	images = all_images.exclude(id=image1_id)
	return render(request, 'polls/start_story_2.html', {
		'user_log': request.user.is_authenticated,
		'first_image_id': image1_id,
		'images': images,
		})


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

