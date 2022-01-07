from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('manage-user/', include('manage_user.urls')),
    path('', include('ege_tests.urls'))
]
