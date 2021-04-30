from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import profile, Blogs, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email' ]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image']  
  
# creating a form 
class UploadForm(ModelForm): 
  
    # create meta class 
    class Meta: 
        # specify model to be used 
        model = Blogs 
		#fields = '__all__'
		
        # specify fields to be used 
        fields = [ 
            "title", 
            "ingredients", 
			"recipe", 
			"ImageorVideo"
        ]
