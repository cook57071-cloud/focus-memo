from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('memo/', include('memo.urls')),   # 메모 앱
    path('accounts/', include('django.contrib.auth.urls')),  # 로그인/로그아웃
]
