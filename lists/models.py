from django.db import models
import datetime
from datetime import date
from django.utils import timezone

class List(models.Model):
	name = models.CharField(max_length=50,unique=True)
	
	def __str__(self):
		return str(self.name)

DONE_CHOICES = ( (0, ''), (1, 'DONE'), (2, 'CANCELLED'), )
	
class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)
	created_date = models.DateTimeField(default = timezone.now)
	done = models.IntegerField(choices = DONE_CHOICES, default=0)
	done_date = models.DateTimeField(null=True)
	
	def __str__(self):
		return self.text
	
	@property
	def is_today(self):
		now = timezone.now()
		if now.day == self.done_date.day:
			if now.month == self.done_date.month:
				if now.year == self.done_date.year:
					return True	
		return False

	  

