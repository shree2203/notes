from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),   # Auth endpoints
    path("api/notes/", include("notes.urls")),  # Notes endpoints
]
