from django.db import models
from djgeojson.fields import MultiPolygonField
from performance.models import EPSA

class SupplyArea(models.Model):
    epsa = models.ForeignKey(
        to=EPSA,
        on_delete=models.CASCADE,
        help_text='Epsa que presta los servicios en esta área.'
    )
    area= models.FloatField(blank=True, null=True)
    geom = MultiPolygonField(blank=True, null=True)

    class Meta:
        verbose_name = 'Área de Prestación de Servicio'
        verbose_name_plural = 'Áreas de Prestación de Servicio'
        ordering = ['epsa__category', 'epsa__code',]

    def __str__(self):
        return f'({self.id}) {self.epsa}'

    def get_category(self):
        return self.epsa.category
    get_category.short_description = 'Categoría'
    def get_state(self):
        return self.epsa.state
    get_state.short_description = 'Departamento'