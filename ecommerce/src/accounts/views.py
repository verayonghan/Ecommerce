from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import LoginForm, RegisterForm, GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail


# Create your views here.

def guest_register_view(request):
	guest_form = GuestForm(request.POST or None)

	context = {
		"form" : guest_form
	}

	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None

	if guest_form.is_valid():
		email = guest_form.cleaned_data.get("email")
		guest_email = GuestEmail.objects.create(email=email)
		request.session['guest_email_id'] = guest_email.id

		if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
		else:
				return redirect("/register/")
	else:
			print("Error") 
	return redirect("/register/")




def login_page(request):
	login_form = LoginForm(request.POST or None)

	context = {
		"title" : "Login page",
		"content" : "Welcome to the login page.",
		"form" : login_form
	}

	print("User logged in")
	print(request.user.is_authenticated) # by django

	next_ = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_path = next_ or next_post or None
	print(redirect_path)
	if login_form.is_valid():
		print(login_form.cleaned_data)

		username = login_form.cleaned_data.get("username")
		password = login_form.cleaned_data.get("password")

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			try:
				del request.session['guest_email_id']
			except:
				pass
        		
			if is_safe_url(redirect_path, request.get_host()):
				return redirect(redirect_path)
			else:
				return redirect("/")
		else:
			print("Error")
			# Return an 'invalid login' error message.


	return render(request, "accounts/login.html", context)



User = get_user_model()
def register_page(request):

	register_form = RegisterForm(request.POST or None)

	context = {
		"title" : "Register page",
		"content" : "Welcome to the register page.",
		"form" : register_form
	}
	
	if register_form.is_valid():
		print(register_form.cleaned_data)
		username = register_form.cleaned_data.get("username")
		email = register_form.cleaned_data.get("email")
		password = register_form.cleaned_data.get("password")
		new_user = User.objects.create_user(username, email, password)
		print(new_user)

	return render(request, "accounts/register.html", context)



