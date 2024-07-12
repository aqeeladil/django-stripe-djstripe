
from django.shortcuts import render, get_object_or_404, redirect
# from django.shortcuts import render, redirect   #crm
# from .models import Tweet
# from .models import Record     #crm
from .forms import UserRegistrationForm
# from .forms import TweetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages   
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
# Create your views here.

def home(request):
    context = {
        # 'BASIC_MONTHLY': os.environ['PREMIUM_MONTHLY'],

        'BASIC_MONTHLY': settings.BASIC_MONTHLY,
        'BASIC_YEARLY': settings.BASIC_YEARLY,
        'PREMIUM_MONTHLY': settings.PREMIUM_MONTHLY,
        'PREMIUM_YEARLY': settings.PREMIUM_YEARLY,
        'ENTERPRISE_MONTHLY': settings.ENTERPRISE_MONTHLY,
        'ENTERPRISE_YEARLY': settings.ENTERPRISE_YEARLY,
    }
    return render(request, 'home.html', context)


def login_user(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		# Authenticate
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, "You Have Been Logged In!")
			return redirect('home')
		else:
			messages.success(request, "There Was An Error Logging In, Please Try Again...")
			return redirect('home')
	else:
            return render(request, 'registration/login.html')


# crm
def register_user(request):
    if request.method == 'POST':
          form = UserRegistrationForm(request.POST)
          if form.is_valid():
               user = form.save(commit=False)
               user.set_password(form.cleaned_data['password1'])

            #    # Authenticate and login
            #    username = form.cleaned_data['username']
            #    email = form.cleaned_data['email']
            #    password = form.cleaned_data['password1']
            #    user_auth = authenticate(username=username, email=email, password=password)

               user.save()
               login(request, user)
               messages.success(request, "You Have Successfully Registered! Welcome!")

               return redirect('home')
    else:
          form = UserRegistrationForm()
          return render(request, 'registration/register.html', {'form':form})
     
    return render(request, 'registration/register.html', {'form':form})


def logout_user(request):
	logout(request)
	messages.success(request, "You Have Been Logged Out...")
	return redirect('home')
















