from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
User = settings.AUTH_USER_MODEL
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
from django.core.exceptions import ValidationError


def validate_image(image):
    file_size = image.file.size
    limit_kb = 150
    if file_size > limit_kb * 1024:
        raise ValidationError("Max size of file is %s KB" % limit)

    #limit_mb = 8
    #if file_size > limit_mb * 1024 * 1024:
    #    raise ValidationError("Max size of file is %s MB" % limit_mb)
# Create your models here.
class profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'profile')
	image = models.ImageField(default= 'default.png',upload_to= 'Profilepics')

	def __str__(self):
		return 'self.user.profile'



class Blogs(models.Model):
	# fields of the model 
    
    title = models.CharField(max_length = 25) 
    ingredients = models.TextField() 
    recipe = models.TextField()
    ImageorVideo = models.FileField( upload_to= 'Blog')
    Author = models.ForeignKey(User, default=1, null = True, on_delete=models.CASCADE)
    created_date = models.DateTimeField('date created', default=timezone.now)


    # with their title name 
    def __str__(self): 
        return self.title 


class Review(models.Model):
    blog = models.ForeignKey(Blogs,default=1, null = True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=1, null = True, on_delete=models.CASCADE)
    comment = models.TextField(max_length=5000, null = True)
    rating = models.FloatField(default=0)
    pub_date = models.DateTimeField('date created', default=timezone.now)

    def __str__(self):
        return self.user.username