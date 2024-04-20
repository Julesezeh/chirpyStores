from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, SubscribedUsers
from django.contrib import messages
from uuid import uuid4
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django.conf import settings
import requests, json
from django.core.serializers.json import DjangoJSONEncoder

def signup(request):
    if request.method == "POST":
        email = request.POST.get("register-email", "")
        password = request.POST.get("register-password", "")
        phone_number = request.POST.get("mobile_number",None)
        username = uuid4()
        
        # Check if the user already exists
        existing_user = CustomUser.objects.filter(email=email).exists()
        print("This bit worked, existing user: ", existing_user)
        
        if not existing_user:
            # Create a new user
            user = CustomUser.objects.create_user(username=username,email=email, password=password)
            
            
            # Authenticate and log in the user
            user = authenticate(request,username=username, email=email, password=password)
            
            if user is not None:
                # Log in the user
                login(request, user)
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                elif "next" in request.GET:
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("MAIN:home")

            else:
                # Authentication failed, handle appropriately
                print("Authentication failed")
                error = "Authentication failed"
                # Redirect or render an error page
        else:
            # User already exists, handle appropriately
            print("User already exists")
            error = "User already exists"
        return render(request,'ERRORS/user_errors.html',{"user_error":error})
            



def login_view(request):
    if request.method == "POST":
        print("request received")
        email = request.POST.get("signin-email", "")
        password = request.POST.get("signin-password", "")
        
        # Check if a user with the provided email exists
        print("this point is okay")
        try:
            user_id = get_object_or_404(CustomUser,email=email)
            print("user_id", user_id)

            user = authenticate(request, username=user_id.username, email=email, password=password)
            print("POSTT",request.POST)
            print("EMAILLLL", email)
            print("PASSWORDDD", password)
            print("USEERRRRRR",user)
            
            if user is not None:
                # User exists and password matches, log in the user
                login(request, user)
                if "next" in request.POST:
                    return redirect(request.POST.get("next"))
                elif "next" in request.GET:
                    return redirect(request.GET.get("next"))
                else:
                    return redirect("MAIN:home")
            else:
                # User doesn't exist or password is incorrect
                messages.error(request, "Invalid email or password. Please try again.")
                error = "Invalid email or password. Please try again."
                return render(request,'login.html',{"user_error":error})
        except Exception as e:
            print("except block")
            print(e)
                       
    # If not a POST request, render the login form
    return render(request, 'login.html')  # Make sure you have a login.html template

        




def subscribe(request):
    if request.method == "POST":
        email  = request.POST.get("user-email")
        print("email",email)
        new_subscribed_user = SubscribedUsers(email=email)
        if new_subscribed_user:
            new_subscribed_user.save()
            return redirect("MAIN:home")
        



def logout_view(request):
    logout(request)
    return redirect("MAIN:home")

    

def google_login(request):
    # Redirect users to Google authentication page
    redirect_uri = request.build_absolute_uri('/auth/login/google/callback/')
    authorization_url = f'https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&redirect_uri={redirect_uri}&response_type=code&scope=openid%20email%20profile'
    return redirect(authorization_url)

def google_callback(request):
    # Exchange authorization code for access token
    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri('/auth/login/google/callback/')
    token_url = 'https://oauth2.googleapis.com/token'
    token_data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',
    }
    token_response = requests.post(token_url, data=token_data)
    token = token_response.json().get('id_token')

    # Validate token
    try:
        idinfo = id_token.verify_oauth2_token(token, Request(), settings.GOOGLE_OAUTH2_CLIENT_ID)
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
    except ValueError:
        return redirect('/')

    # You can now use idinfo['email'] or idinfo['sub'] (unique Google user ID) to identify the user
    # Example:
    # Get the user object from the tuple returned by get_or_create
    user, created = CustomUser.objects.get_or_create(email=idinfo['email'])
    print("user",user)
    print("user pk", user.pk)

    # Serialize the primary key using Django's JSON encoder
    request.session["SESSION_KEY"] = json.dumps(user.pk, cls=DjangoJSONEncoder)
 
    login(request, user)


    return redirect('/')