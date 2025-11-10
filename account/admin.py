from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # فیلدهای قابل نمایش در صفحه ویرایش
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('اطلاعات شخصی', {'fields': ('first_name', 'last_name', 'email')}),
        ('مجوزها', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_author',
                'special_user',
                'groups',
                'user_permissions',
            ),
        }),
        ('تاریخ‌ها', {'fields': ('last_login', 'date_joined')}),
    )

    # ستون‌های نمایش داده شده در لیست کاربران
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_author',
        'is_special_user',
    )

    # فیلدهای قابل جستجو
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_author', 'groups')
    ordering = ('username',)
