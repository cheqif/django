from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('问题',               {'fields': ['question_text']}),
        ('日期', {'fields': ['pub_date']}),
        ('是否有效', {'fields': ['is_active']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently','was_active')
    list_filter = ['pub_date','is_active']
    search_fields = ['question_text','is_active']


admin.site.register(Question, QuestionAdmin)