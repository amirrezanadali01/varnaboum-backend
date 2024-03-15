from django.contrib import admin

from ticket.models import MessageTicketModel, TicketModel


class TicketModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'isfinish',
                    'office', 'personal', 'date')
    list_filter = ('isfinish',)
    search_fields = ('name', 'office__name')


class TicketMessageModelAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'date',)

    search_fields = ('ticket__name',)


admin.site.register(MessageTicketModel, TicketMessageModelAdmin)
admin.site.register(TicketModel, TicketModelAdmin)
