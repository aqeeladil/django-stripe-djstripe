from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class Record(models.Model):
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	first_name = models.CharField(max_length=50)
# 	last_name =  models.CharField(max_length=50)
# 	email =  models.CharField(max_length=100)
# 	phone = models.CharField(max_length=15)
# 	address =  models.CharField(max_length=100)
# 	city =  models.CharField(max_length=50)
# 	state =  models.CharField(max_length=50)
# 	zipcode =  models.CharField(max_length=20)

# 	def __str__(self):
# 		return(f"{self.first_name} {self.last_name}")
	

# class Tweet(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField(max_length=150)
#     photo = models.ImageField(upload_to="")
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.text[:10]}"