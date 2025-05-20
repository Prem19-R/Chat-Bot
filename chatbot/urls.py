from django.urls import path
from .views import chat_api, chatbot_home,login_view,register,user_logout,chat_history,about

urlpatterns = [
    path("", chatbot_home, name="chatbot_home"),  
    path("api/chat/", chat_api, name="chat_api"), 
    path('login/', login_view, name='login'),
    path("register/", register, name="register"),
    path("logout/", user_logout, name="logout"),
    path("history/", chat_history, name="chat_history"),
    path("about/",about,name='about')
]
