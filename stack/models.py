from email.mime import image
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.

from django.contrib.auth.models import User

class Questions(models.Model):
    question=models.CharField(max_length=500)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="image",null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    is_active=models.BooleanField(default=True)

    @property
    def fetch_answers(self):
        answers=self.answer_set.all().annotate(up_count=Count('up_vote')).order_by('-up_count')
        return answers

    def str(self):
        return self.question

class Answer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    answer=models.CharField(max_length=500)
    Question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    created_date=models.DateField(auto_now_add=True)
    up_vote=models.ManyToManyField(User,related_name="upvotes")

    def up_vote_count(self):
        return self.up_vote.all().count()

    def str(self):
        return self.answer