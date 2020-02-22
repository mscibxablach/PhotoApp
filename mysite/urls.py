from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),

    # FOR PHOTOS
    # views.photo_list -> pobieranie widoku pod dany url
    path('photos/', views.photo_list, name='photo_list'),
    path('photos/upload/', views.upload_photo, name='upload_photo'),
    # int:pk - primary key of photo
    path('photos/<int:pk>/', views.delete_photo, name='delete_photo'),

    path('admin/', admin.site.urls),

    # ONLY FOR CREATING PDF
    path('upload_photo_without_DB/', views.upload_photo_without_DB, name='upload_photo_without_DB'),

    path('pdf', views.some_view),
]

# tylko do developmentu
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
