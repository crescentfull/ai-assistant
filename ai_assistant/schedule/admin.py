from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Schedule, Tag

class CustomUserAdmin(UserAdmin):
    # 사용자 목록에 표시할 필드
    list_display = ('username', 'email', 'student_id', 'is_bt_student', 'is_staff', 'is_active')
    # 필터 옵션 설정
    list_filter = ('is_bt_student', 'is_staff', 'is_active')
    # 사용자 상세 화면 필드
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields':
                                   ('first_name', 'last_name', 'email',
                                    'student_id', 'is_bt_student')
                          }
        ),
        ('Permissions', {'fields': 
                                ('is_active', 'is_staff', 'is_superuser',
                                 'groups', 'user_permissions')
                        }
        ),
        ('Important dates', {'fields': 
                                    ('last_login', 'date_joined')
                            }
        ),
    )
    # 사용자 생성 화면에서 필드 분류
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2',
                       'student_id', 'is_bt_student', 'is_active',
                       'is_staff', 'is_superuser', 'groups', 'user_permissions'),
                }
        ),
    )
    # 검색 필드 설정
    search_fields = ('username', 'email', 'student_id')
    # 정렬 기준 설정
    ordering = ('username',)
    
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Schedule)
admin.site.register(Tag)