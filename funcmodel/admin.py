from django.contrib import admin
from .models import Function
from .tasks import update_plot


def refresh_selected_functions(admin, request, queryset):
    for obj in queryset:
        update_plot.apply_async((obj.id,), expires=5)#apply_async

class FunctionAdmin(admin.ModelAdmin):
    list_display = ('signature', 'plot_img', 'interval', 'steep', 'processing')
    exclude = ('plot_img',)
    actions = (refresh_selected_functions,)


    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()





admin.site.register(Function, FunctionAdmin)