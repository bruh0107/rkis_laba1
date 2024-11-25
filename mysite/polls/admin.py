from django.contrib import admin
from .models import Question, Choice


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'is_active')
    list_filter = ('pub_date',)
    search_fields = ('question_text',)

admin.site.register(Question, QuestionAdmin)
