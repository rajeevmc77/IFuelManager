
from django.contrib import admin
from django.urls import path
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from dashboard.views import DashboardView

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', include('obdService.urls'))
    path('', DashboardView.as_view(), name="DashboardView"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)