# payments/admin.py
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'verified', 'reference', 'created_at')
    search_fields = ('user__email', 'reference')
    list_filter = ('status', 'verified', 'created_at')
from django.contrib import admin

# Register your models here.
