from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register, name="register"),
    path('login/', views.Login, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
    path('edit-task/<int:pk>/update', views.EditTask, name='edit'),
  
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)