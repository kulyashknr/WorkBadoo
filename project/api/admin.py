from django.contrib import admin
from .models import MainUser, Worker, Company, Vacancy, Matching, MatchingForCompany, MatchingForWorker
from django.contrib.auth.admin import UserAdmin

@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    list_display = ('id', 'username', )


admin.site.register(Worker)
admin.site.register(Company)
admin.site.register(Vacancy)
admin.site.register(Matching)
admin.site.register(MatchingForWorker)
admin.site.register(MatchingForCompany)