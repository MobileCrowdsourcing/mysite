# from django.db import models
# from django.utils.encoding import python_2_unicode_compatible
# from django.utils import timezone
# import datetime


# @python_2_unicode_compatible
# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
    
#     def __str__(self):
#         return self.question_text
    
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)

#     def __str__(self):
#         return self.choice_text



from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime
from django.utils import timezone


@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
   
    def __str__(self):
        return self.question_text
        
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
        # return self.pub_date>=timezone.now()-datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Scenario(models.Model):
    scenario_text = models.CharField(max_length=300)

    def __str__(self):
        return self.scenario_text


@python_2_unicode_compatible
class Text_Input(models.Model):
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    input_text = models.TextField()

    def __str__(self):
        return self.input_text


class Link(models.Model):
    scenario_from = models.ForeignKey(Scenario, related_name='f_link', on_delete=models.CASCADE)
    link_path = models.ForeignKey(Text_Input, on_delete=models.CASCADE)
    scenario_to = models.ForeignKey(Scenario, related_name='b_link', on_delete=models.CASCADE)

    popularity = models.IntegerField(default=1)

    def __str__(self):
        return (str(self.scenario_from.id) + ' -- ' + str(self.link_path.id) + '-->' + str(self.scenario_to.id))


