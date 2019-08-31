# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Base(models.Model):
	class Meta:
		abstract = True
	
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name


class Board(Base):
	owner = models.ForeignKey(User)


class Task(Base):
	board = models.ForeignKey(Board)


class Card(Base):
	description = models.CharField(max_length=1000)
	deadline = models.DateTimeField()
	task = models.ForeignKey(Task)
