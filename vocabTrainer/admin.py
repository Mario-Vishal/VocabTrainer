from django.contrib import admin
from .models import VocabCard,TempDeck, Streak
# Register your models here.
admin.site.register(VocabCard)
admin.site.register(TempDeck)
admin.site.register(Streak)
    