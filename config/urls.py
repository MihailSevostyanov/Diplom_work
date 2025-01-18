from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from profitpages.views import upload_file

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls", "users")),
    path("", include("profitpages.urls", "main")),
    path("image_upload/", upload_file, name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
