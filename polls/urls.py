# from django.conf.urls import url

# from . import views

# app_name = 'polls'
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
#     url(r'pengu/', views.pengu, name='pengu'),
#     url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
#     # ex: /polls/5/vote/
#     url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote')
#     ]

from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'pengu/', views.pengu, name='pengu'),
    url(r'scenario/$', views.narration, name='scenarios'),
    url(r'scenario/(?P<sc_id>[0-9]+)/make$', views.make_scenario, name='make_scenario'),
    url(r'scenario/(?P<sc_id>[0-9]+)/create_path$', views.create_path, name='create_path'),
    url(r'scenario_link/(?P<flag>[0-3])/$', views.make_scenario_link, name='make_scenario_link'),
    url(r'scenario_link/(?P<flag>[0-3])/(?P<sc_id>[0-9]+)/$', views.make_scenario_link, name='choose_path'),
    url(r'scenario_link/(?P<flag>[0-3])/(?P<sc_id>[0-9]+)/(?P<path_id>[0-9]+)/$', views.make_scenario_link, name='choose_dest'),
    url(r'scenario_link/(?P<flag>[0-3])/(?P<sc_id>[0-9]+)/(?P<path_id>[0-9]+)/(?P<sc_t_id>[0-9]+)$', views.make_scenario_link, name='mk_2'),
    url(r'get_image/$',views.link_images,name='link_images'),
    url(r'update_link/(?P<link_id>[0-9]+)/$', views.update_link, name='update_link'),
    url(r'view_links/$', views.view_image_links, name='view_image_links'),
    url(r'pic/(?P<im_link_id>[0-9]+)/$', views.vote_link, name='vote_link'),
    url(r'choose_chain/$', views.show_chains, name='choose_chain'),
    url(r'choose_image/$', views.choose_image, name='choose_image'),
    url(r'choose_image/(?P<chain_id>[0-9]+)/$', views.choose_image, name='choose_2image'),
    url(r'check_chain/(?P<chain_id>[0-9]+)/$', views.check_chain, name='check_chain'),
    url(r'start_story/$', views.start_story, name='start_story'),
    url(r'start_story_2/$', views.start_story_2, name='start_story_2'),
    url(r'add_story/(?P<first_image_id>[0-9]+)/$', views.add_story, name='add_story'),
    url(r'add_base/$', views.add_base, name='add_base'),
    url(r'make_sequence/$', views.make_sequence, name='make_sequence'),
    url(r'select_story/(?P<base_id>[0-9]+)/$', views.select_story, name='select_story'),
    url(r'story_redirect/$', views.story_redirect, name='story_redirect'),
    url(r'add_action/(?P<story_id>[0-9]+)/$', views.add_action, name='add_action'),
    url(r'continue_story/(?P<story_id>[0-9]+)/$', views.continue_story, name='continue_story'),
    url(r'add_success/(?P<story_id>[0-9]+)/$', views.add_success, name='add_success'),
    url(r'show_stories/$', views.show_stories, name='show_stories'),
    url(r'work_story/$', views.work_story, name='work_story'),
    url(r'read_stories/(?P<story_id>[0-9]+)/$', views.read_stories, name='read_stories'),
    url(r'write_story/(?P<story_id>[0-9]+)/$', views.write_story, name='write_story'),
    url(r'add_action_image/(?P<story_id>[0-9]+)/$', views.add_action_image, name='add_action_image'),
  #  url(r'add_action/(?P<story_id>[0-9]+)/own_image/$', views.add_action_image, name='add_action_image'),
    
]
