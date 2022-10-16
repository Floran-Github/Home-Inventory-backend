from django.contrib import admin
from .models import *

admin.site.register(TransactionItem)
admin.site.register(TransactionRecord)
admin.site.register(Market)