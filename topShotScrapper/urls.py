from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import topShotListView, topShot_detail, setView, challengeView, set_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', topShotListView.as_view(), name = 'ts-item-list'),
    path('challenges/', challengeView.as_view(), name = 'set-item-list'),
    path('sets/', setView.as_view()),
    path('<id>/', topShot_detail),
    path('sets/<id>/', set_detail),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

