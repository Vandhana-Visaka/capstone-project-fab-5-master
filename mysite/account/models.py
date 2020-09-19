from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime


class MyAccountManager(BaseUserManager):
	'''
	User Authetication and Log In
	'''
	def create_user(self, email, username, firstname, lastname, gender, birthday, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			firstname=firstname,
			lastname=lastname,
            gender=gender,
			birthday=birthday,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username,password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
			firstname='Mark',
			lastname='Han',
            gender='Male',
            birthday='2006-10-25',
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	'''
	Allows users to create account and access services
	Application keeps track of log in and activity
	'''
	email 					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username 				= models.CharField(max_length=30, unique=True)
	firstname               = models.CharField(verbose_name="firstname", max_length=30)
	lastname                = models.CharField(verbose_name="lastname", max_length=30)
	GENDER_CHOICES = (('Male', 'M'),('Female', 'F'),('Other','O'))
	gender 					= models.CharField(max_length=10,choices=GENDER_CHOICES)
	birthday                = models.DateField(verbose_name='birthday')
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	similar_users 			= models.TextField(null=True, blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True
