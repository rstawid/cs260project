from django.db import models
import datetime

class List(models.Model):
	name = models.CharField(max_length=50,unique=True)
#	title = models.CharField(max_length=250, unique=True, default='')
	
	def __str__(self):
		return str(self.name)

DONE_CHOICES = ( (0, ''), (1, 'DONE'), (2, 'CANCELLED'), )
	
class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)
	created_date = models.DateTimeField(default=datetime.datetime.now)
	done = models.IntegerField(choices = DONE_CHOICES, default=0)
	done_date = models.DateTimeField(blank=True)
	
	def __str__(self):
		return self.text
	
	@property
	def is_today(self):
		now = datetime.datetime.now()
		today = datetime.datetime.today()
		if today.day == self.done_date.day:
			return True	
		return False

	  

