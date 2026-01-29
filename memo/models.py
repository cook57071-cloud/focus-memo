from django.db import models
from django.conf import settings  # User 모델 가져오기 위해

class Memo(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='memos',
        verbose_name='작성자'
    )
    content = models.TextField(verbose_name='메모 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일시')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일시')
    keywords = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='키워드 (자동 생성 예정)'
    )

    class Meta:
        ordering = ['-created_at']          # 최신순 정렬 기본값
        verbose_name = '메모'
        verbose_name_plural = '메모 목록'

    def __str__(self):
        return f"{self.author.username}의 메모 ({self.created_at.date()})"