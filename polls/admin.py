from django.contrib import admin
from .models import Choice, Question, QuestionUser


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionUserInline(admin.TabularInline):
    model = QuestionUser
    filter_horizontal = ('user',)
    max_num = 1
    min_num = 1
    extra = 1
    #def has_add_permission(self, request):
    #    return False

    def has_delete_permission(self, request, obj=None):
        return False


class QuestionAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(QuestionAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(user=request.user)

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def save_model(self, request, obj, form, change):
        """  重新定义此函数，提交时自动添加申请人和备案号  """
        obj.user = request.user
        super(QuestionAdmin, self).save_model(request, obj, form, change)

    readonly_fields = ('user',)
    fieldsets = [
        ('基本信息', {'fields': [('question_text', 'is_active')]}),
        ('发布时间', {'fields': ['pub_date']}),
        ('投票时间段', {'fields': [('start_date', 'end_date')]}),
        ('投票票数设置', {'fields': [('min_select', 'max_select')]}),
        ('用户', {'classes': ['collapse'], 'fields': ['user']}),
    ]
    inlines = [ChoiceInline, QuestionUserInline]
    list_display = ('questions', 'pubdate', 'was_published_recently','was_active','author_name')
    list_per_page = 10
    list_filter = ['pub_date', 'is_active']
    search_fields = ['question_text', 'is_active']


admin.site.register(Question, QuestionAdmin)
