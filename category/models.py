from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'category'

    #to avoid loop in inheritance
    def clean(self):
        if not self.parent:
            return

        # خودش والد خودش نشود
        if self.parent == self:
            raise ValidationError("A category cannot be its own parent.")

        # یکی از فرزندانش والدش نشود
        parent = self.parent
        while parent:
            if parent == self:
                raise ValidationError(
                    "A category cannot have one of its descendants as parent."
                )
            parent = parent.parent

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_all_attributes(self):
        attributes = list(self.attributes.all())
        if self.parent:
            attributes += self.parent.get_all_attributes()
        return attributes

    def get_full_path(self):
        if self.parent:
            return f'{self.parent.get_full_path()} > {self.name}'
        return self.name
    
    def __str__(self):
        return self.get_full_path()
    
    def get_descendants_ids(self):
        ids = [self.id]

        for child in self.children.all():
            ids.extend(child.get_descendants_ids())

        return ids
    
class CategoryAttribute(models.Model):
    ATTRIBUTE_TYPES = [
        ('text', 'متن'),
        ('number', 'عدد'),
        ('boolean', 'بله/خیر'),
        ('select', 'انتخابی'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='attributes')
    name = models.CharField(max_length=50)
    attribute_type = models.CharField(max_length=20, choices=ATTRIBUTE_TYPES, default='text')
    unit = models.CharField(max_length=20, null=True, blank=True)
    is_filter = models.BooleanField(default=False)
    is_required = models.BooleanField(default=False)

    class Meta:
        db_table = 'category_attribute'

    def __str__(self):
        return f'{self.category.name}-{self.name}'