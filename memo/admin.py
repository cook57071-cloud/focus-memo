from django.contrib import admin
from .models import Memo  # Memo 모델 가져오기

# Memo 모델을 관리자 페이지에 등록
admin.site.register(Memo)
