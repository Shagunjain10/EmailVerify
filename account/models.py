from django.db import models
from django.contrib.auth.models import User

# User._meta.get_field('email')._unique = True
# User._meta.get_field('email').blank = False
# User._meta.get_field('email').null = False

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
	isVerified=models.BooleanField(default=False)
	# name = models.CharField(max_length=100, default="Unknown", blank=True)
	# email = models.EmailField(blank=True, null=True)
	# phone_regex = RegexValidator(
	# 	regex=r'^[6-9]{1}[0-9]{9}$', message="Phone number should in the format: '999999999'. Exactly 10 digits allowed. First digit can be 6,7,8,9")
	# phoneNumber = models.CharField(validators=[phone_regex], max_length=10, blank=True)
	# gender = models.CharField(max_length=30, choices=GENDER, blank=True, null=True)
	# category=models.CharField(max_length=30, choices=CATEGORY, blank=True, null=True)
	createdAt=models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username