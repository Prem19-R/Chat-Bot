from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer
from .chatbot_logic import chatbot_response
import json
from django.contrib.auth import  logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm

@csrf_exempt  # Disable CSRF for this view

def about(request):
    return render(request, "chatbot/about.html")

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect("home")  # Redirect to home page after login
    else:
        form = CustomUserCreationForm()
    
    return render(request, "chatbot/register.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("chatbot_home")

def chat_history(request):
        chats = Chat.objects.filter(user=request.user).order_by('-timestamp')  # Show only user's history
        return render(request, 'chatbot/history.html', {'chats': chats})
   # chats = Chat.objects.all().order_by('-timestamp')  # Fetch chats in reverse order

@login_required
def chatbot_home(request): 
    """
    Render chatbot page with chat history for logged-in users.
    """
    chat_history = Chat.objects.filter(user=request.user).order_by("-id")[:10]  # Load last 10 messages
    return render(request, "chatbot/chat.html", {"chat_history": chat_history})

@api_view(["POST"])
@permission_classes([IsAuthenticated])  # Ensure only logged-in users can access
def chat_api(request): 
    """
    API endpoint to handle chatbot interaction.
    """
    user_message = request.data.get("message", "").strip()
    if not user_message:
        return Response({"error": "No message provided"}, status=400)

    bot_reply = chatbot_response(user_message)  # Get chatbot response

    # Save chat history
    chat_instance = Chat.objects.create(user=request.user, user_input=user_message, bot_response=bot_reply)
    serializer = ChatSerializer(chat_instance)

    return Response({"response": bot_reply})  # Send JSON response

def login_view(request):
    """
    Handles user login.
    """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("chatbot_home")  # Redirect to chatbot after login
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

