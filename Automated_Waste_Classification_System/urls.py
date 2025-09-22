from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. Default Django Admin Panel (http://127.0.0.1:8000/admin/)
    path('admin/', admin.site.urls),

    # 2. Root URL → Redirects to login page automatically
    path('', lambda request: redirect('login')),

    # 3. Include all URLs from waste_classifier app (register, login, home, etc.)
    path('', include('waste_classifier.urls')),
]

# 4. To serve uploaded files (images) during development
# Example: when user uploads waste image, we need MEDIA_URL + MEDIA_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
