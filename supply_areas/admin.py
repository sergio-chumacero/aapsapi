from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from supply_areas.models import SupplyArea

@admin.register(SupplyArea)
class SupplyAreaModelAdmin(LeafletGeoAdmin):
    view_on_site = False
    list_filter= ('epsa__category', 'epsa__state', 'epsa',)
    search_fields= ['epsa__code', 'epsa__name', 'epsa__state',]
    list_display= ('epsa', 'get_category', 'get_state',)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS: Áreas de Prestación de Serivicios de las EPSA Reguladas'}
        return super(SupplyAreaModelAdmin, self).changelist_view(request, extra_context=extra_context)


