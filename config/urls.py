from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 이제 같은 층에 있는 memo_app의 주소록을 정확히 바라봅니다.
    path('', include('memo_app.urls')), 
]