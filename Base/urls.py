from django.urls import path
from . import views
urlpatterns = [
    path('',views.SystemDocumentation),
    path('Follow_Profile/<str:pk>/',views.Follow_Profile),
    path('Post_Event/',views.PostEvent),
    path('Enroll_Event/<str:pk>/',views.Enroll_in_Event),
    path('Like_Event/<str:pk>/',views.Like_Event),
    path('Dislike_Event/<str:pk>/',views.Dislike_Event),
    path('Search_Event/',views.search_events_by_title),
    
]
