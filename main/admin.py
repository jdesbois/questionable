from django.contrib import admin
from main.models import Course, Lecture, Question, Reply, Forum, Post, Comment, Student, Tutor, Upvote, Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(Forum)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Upvote)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)