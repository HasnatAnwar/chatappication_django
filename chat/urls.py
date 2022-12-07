from django.urls import path , include
from . import views
urlpatterns = [
    path('index/',views.index),
    path('signup',views.sign_up),
    path('signin',views.sign_in),
    path('profile',views.profile),
    path('profilee',views.profilee),
    path('other/<int:id>',views.otherprofile),
    path('conservation',views.conservation),
    path('chat/<int:id>',views.chat),
    

]
