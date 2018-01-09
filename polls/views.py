from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.template import loader
from .models import Question, Choice, Scenario, Text_Input, Link
from django.views import generic
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



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


def login_user(request):

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse('polls:index'))
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


def make_link(request, flag=0, sc_id=None, path_id=None, sc_t_id=None):

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
