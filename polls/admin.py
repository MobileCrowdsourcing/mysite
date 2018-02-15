from django.contrib import admin

# Register your models here.

from .models import Question, Choice, Scenario, Text_Input, Link, ImageScenario, ImageLink, ImageChain, BaseImage, ActionImage
from .models import Story, Authors, StoryText, Feedback


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    # fields = ['pub_date', 'question_text']


class Text_InputInline(admin.TabularInline):
	model = Text_Input
	extra = 1


class ScenarioAdmin(admin.ModelAdmin):
	# fieldsets = [
 #        (None,               {'fields': ['scenario_text']})
 #    ]
    
    fieldsets = [
    	(None,	{'fields': ['scenario_text']})
    ]
    inlines = [Text_InputInline]
    # inlines = [Text_InputInline]
    list_display = ('scenario_text',)
    search_fields = ['scenario_text']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(Text_Input)
admin.site.register(Link)
admin.site.register(ImageScenario)
admin.site.register(ImageLink)
admin.site.register(ImageChain)
admin.site.register(BaseImage)
admin.site.register(ActionImage)
admin.site.register(Story)
admin.site.register(Authors)
admin.site.register(StoryText)
admin.site.register(Feedback)