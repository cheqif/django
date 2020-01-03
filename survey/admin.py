from django.contrib import admin
from .models import SurveyChoice, SurveyQuestion, SurveyUser, Survey
import nested_admin


class SurveyChoiceInline(nested_admin.NestedTabularInline):
    model = SurveyChoice
    extra = 3


class SurveyQuestionInline(nested_admin.NestedStackedInline):
    model = SurveyQuestion
    inlines = [SurveyChoiceInline, ]
    extra = 1


class SurveyUserInline(nested_admin.NestedTabularInline):
    model = SurveyUser
    filter_horizontal = ('user',)
    max_num = 1
    min_num = 1
    extra = 1
    #def has_add_permission(self, request):
    #    return False

    def has_delete_permission(self, request, obj=None):
        return False


class SurveyAdmin(nested_admin.NestedModelAdmin):
    def get_queryset(self, request):
        ss = super(SurveyAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return ss
        else:
            return ss.filter(user=request.user)

    def has_delete_permission(self, request, obj=None):
        # 禁用删除按钮
        return False

    def save_model(self, request, obj, form, change):
        """  重新定义此函数，提交时自动添加申请人和备案号  """
        obj.user = request.user
        super(SurveyAdmin, self).save_model(request, obj, form, change)

    readonly_fields = ('user',)
    fieldsets = [
        ('基本信息', {'fields': [('survey_text', 'is_active')]}),
        ('发布时间', {'fields': ['pub_date']}),
        ('问卷调查时间段', {'fields': [('start_date', 'end_date')]}),
        ('发布者', {'classes': ['collapse'], 'fields': ['user']}),
    ]
    inlines = [SurveyQuestionInline, SurveyUserInline]
    list_display = ('surveys', 'pubdate', 'was_published_recently', 'was_active', 'author_name')
    list_per_page = 10
    list_filter = ['pub_date', 'is_active']
    search_fields = ['survey_text', 'is_active']


admin.site.register(Survey, SurveyAdmin)
