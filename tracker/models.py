from django.db import models
from django.contrib.auth.models import User
import datetime

class Category(models.Model):
    name = models.CharField(max_length=100)
    is_predefined = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='categories')

    def __str__(self):
        return self.name

class Expense(models.Model):
    PAYMENT_METHODS = [
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='Cash')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} - {self.amount}"
    
    class Meta:
        ordering = ['-date', '-created_at']

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='budgets')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField(help_text="Set to the first day of the month")

    def __str__(self):
        scope = self.category.name if self.category else "Overall"
        return f"{self.user.username} - {scope} Budget for {self.month.strftime('%b %Y')}"

    class Meta:
        unique_together = ('user', 'category', 'month')
