from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app_name.urls')),  # Replace 'your_app_name' with the actual app name
]