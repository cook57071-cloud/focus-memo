from django.db import models
from django.contrib.auth.models import User

class Memo(models.Model):
    CATEGORY_CHOICES = [
        ('life', '생활'),
        ('work', '업무'),
        ('study', '학습'),
        ('event', '이벤트'),
        ('temp', '임시'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    category = models.CharField(
        max_length=10, 
        choices=CATEGORY_CHOICES, 
        default='temp',
        verbose_name='카테고리'
    )
    confidence = models.FloatField(default=0.0, verbose_name='예측 신뢰도')
    keywords = models.CharField(max_length=200, blank=True, verbose_name='키워드')
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name='작성자'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = '메모'
        verbose_name_plural = '메모들'
    
    def __str__(self):
        return f'{self.title} ({self.get_category_display()})'
    
    def save(self, *args, **kwargs):
        if self.content and len(self.content.strip()) > 5:
            try:
                from .category_predictor import predictor
                predicted_category, confidence = predictor.predict(self.content)
                self.category = predicted_category
                self.confidence = confidence
                self.keywords = predictor.extract_top_keywords(self.content)
            except ImportError:
                pass
        
        super().save(*args, **kwargs)
