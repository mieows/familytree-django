from django.db.models.signals import *
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from familytree.models import *

# Note objects
class Note(models.Model):
	author = models.ForeignKey(User)
	created_date = models.DateTimeField(default=datetime.now)
	title = models.CharField(max_length=50)
	description = models.CharField(max_length=200)

# Picture objects
class Familypicture(models.Model):
	photo = models.ImageField(upload_to='get_profile_path', blank=True, null=True)
	thumbnail = models.ImageField(upload_to='profile_thumb', blank=True, null=True,editable=False)

# Person object
class Person(models.Model):
	# creation info
	author = models.ForeignKey(User)
	created_date = models.DateTimeField(default=datetime.now)

	# Names
	firstname = models.CharField(max_length=20)
	middlename1 = models.CharField(max_length=20, null=True, blank=True)
	middlename2 = models.CharField(max_length=20, null=True, blank=True)
	surname = models.CharField(max_length=20)
	maidenname = models.CharField(max_length=20, null=True, blank=True)
		
	sex = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
	DOB = models.DateField(null=True, blank=True)
	DOD = models.DateField(null=True, blank=True)
		
	# Relations
	parents = models.ManyToManyField("Person", related_name='p', verbose_name="Parents", null=True, blank=True)
	siblings = models.ManyToManyField("Person", related_name='s', verbose_name="Siblings", null=True, blank=True)
	partners = models.ManyToManyField("Person", related_name='ps', verbose_name="Partner", null=True, blank=True)
	children = models.ManyToManyField("Person", related_name='c', verbose_name="Children", null=True, blank=True)
		
	# Notes
	notes = models.ManyToManyField(Note, verbose_name="Notes", null=True, blank=True)
		
	# Pictures
	familypictures = models.ManyToManyField(Familypicture, verbose_name="familypictures", null=True, blank=True)
    
	def __unicode__(self):
		return u'%s %s' % (self.firstname, self.surname)

# after a Person object is saved, want to see if they have filled in any relation fields
# if they have we want to mirror this in the other person object. So for instnace
# if bob sets mary as mother, we will set mary's child relation to show bob. 

# the 'connect_person' function will be called when Person m2m is changed.
def connect_person(sender, instance, action, reverse, model, pk_set, **kwargs):
	print "connect called with action '%s'" %action
	print instance.id
	if action == "pre_clear":	        
		for parent in instance.parents.all():
			print 'clear', parent.firstname
			# if remove bob as parent, then remove user from bobs children
			parent.children.remove(instance)

			# if remove bob as parent, then remove users as siblings of bobs children.
			for child in parent.children.all():
				child.siblings.remove(instance)

	if action == "post_add":
		for parent in instance.parents.all():
			print 'save', parent.firstname
			# when you add Bob as parent, them bob meeds his list of children updated to match this. 
			parent.children.add(instance)                        

			# when you add Bob as parent, them all bobs children need to have this user as there sibling. 
			for child in parent.children.all():
				child.siblings.add(instance)

def connect_siblings(sender, instance, action, reverse, model, pk_set, **kwargs):
	if action == "pre_clear":
	#If I remove Jack as my brother, then remove me from Jacks siblings. 
		for sibling in instance.siblings.all():
			sibling.siblings.remove(instance)
			
	if action == "post_add":
	#If I add Joe as my brother, then need to add me to Joes siblings
		for sibling in instance.siblings.all():
			# test if user is already Joes brother
			try:   
				me =  sibling.siblings.get(id=instance.pk)
			except:
				sibling.siblings.add(instance)

def connect_partner(sender, instance, action, reverse, model, pk_set, **kwargs):        
	if action == "pre_clear":
		for otherHalf in instance.partner.all():
			try:
				me = otherHalf.partner.get(id=instance.pk)
			except:
				otherHalf.partner.remove(instance)

	if action == "post_add":
		for otherHalf in instance.partner.all():
			try:
				me = otherHalf.partner.get(id=instance.pk)
			except:
				otherHalf.partner.add(instance)

m2m_changed.connect(connect_partner, sender=Person.parents.through)
m2m_changed.connect(connect_siblings, sender=Person.siblings.through)
m2m_changed.connect(connect_person, sender=Person.parents.through)
