from django.db import models

# Create your models here.

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general', 'سوال عمومی'),
        ('support', 'پشتیبانی'),
        ('complaint', 'انتقاد'),
        ('suggestion', 'پیشنهاد'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=11, blank=True, null=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.get_subject_display()}'
