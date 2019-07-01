from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from ambiental.models import SARH, TecnicalDataSub, TecnicalDataSup

class TecnicalDataSubInline(admin.StackedInline):
    model = TecnicalDataSub
    extra = 1

class TecnicalDataSupInline(admin.StackedInline):
    model = TecnicalDataSup
    extra = 1

@admin.register(SARH)
class SARHModelAdmin(LeafletGeoAdmin):
    view_on_site = False
    list_filter= ('epsa__category', 'epsa__state', 'epsa','municipality','sub_subt')
    search_fields= ['epsa__code', 'epsa__name', 'epsa__state','user']
    list_display = ('sarh_id','epsa','user','get_state','municipality','get_sub_subt')

    inlines = [TecnicalDataSubInline,TecnicalDataSupInline]

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS: Sistemas de Autoabastecimiento de Recursos Hídricos (SARH).'}
        return super(SARHModelAdmin, self).changelist_view(request, extra_context=extra_context)



