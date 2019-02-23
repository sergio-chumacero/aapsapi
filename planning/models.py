import datetime
from django.db import models
from performance.models import EPSA
from django.core.validators import MinValueValidator, MaxValueValidator

state_code_to_name = {
    'LP': 'La Paz',
    'CO': 'Cochabamba',
    'PO': 'Potosí',
    'SC': 'Santa Cruz',
    'CH': 'Chuquisaca',
    'OR': 'Oruro',
    'TA': 'Tarija',
    'BE': 'Beni',
    'PA': 'Pando',
}

class POA(models.Model):
    '''
    Modelo representando un Presupuesto Operativo Anual (POA) de una EPSA.
    '''
    epsa = models.ForeignKey(
        to=EPSA,
        verbose_name='EPSA',
        on_delete=models.CASCADE,
        related_name='poas',
        help_text='EPSA que reporta el POA'
    )
    year = models.IntegerField(
        verbose_name='Año',
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900)],
        help_text='Año de reporte'
    )
    order = models.IntegerField(
        verbose_name='Orden',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Orden del POA (inicial:1, reprogramado:2-5)'
    )
    
    class Meta:
        unique_together = ('epsa','year','order',)
        verbose_name = 'POA'
        verbose_name_plural = 'POAs'
        ordering = ['epsa__code','year','order',]

    def __str__(self):
        return f'{self.epsa}-{self.year}-{self.order}'
    def get_category(self):
        return self.epsa.category
    get_category.short_description = 'categoría'
    def get_state(self):
        return state_code_to_name[self.epsa.state]
    get_state.short_description = 'departamento'

class Income(models.Model):
    '''
    Modelo representando un ingreso presupuestado en un POA.
    '''
    INCOME_TYPES = (
        ('op_ap', 'Operativos - Agua Potable'),
        ('op_alc', 'Operativos - Alcantarillado'),
        ('op_otros', 'Operativos - Otros'),
        ('no_op', 'No Operativos'),
        ('otros', 'Otros'),
    )
    poa = models.ForeignKey(
        to= POA,
        verbose_name= 'POA',
        on_delete=models.CASCADE,
        related_name='incomes',
        help_text='POA al cual pertenece el ingreso.',  
    )
    income_type = models.CharField(
        verbose_name= 'tipo',
        max_length= 16,
        choices= INCOME_TYPES,
        default='otros',
        help_text= 'Tipo del ingreso.', 
    )  
    description = models.CharField(
        verbose_name= 'descripción',
        max_length= 256,
        help_text= 'Descripción del ingreso.'
    )
    value = models.FloatField(
        verbose_name=f'valor (Bs.)',
        help_text= f'Valor en bolivianos del ingreso.'
    )
    class Meta:
        verbose_name = 'Ingreso POA'
        verbose_name_plural = 'Ingresos POAs'
        ordering = ['poa', 'id',]

    def __str__(self):
        return f'{self.poa} ({self.id})'
    

class Expense(models.Model):
    '''
    Modelo representando un gasto presupuestado en un POA.
    '''
    EXPENSE_TYPES = (
        ('operativos', 'Operativos'),
        ('administrativos', 'Administrativos'),
        ('financieros', 'Financieros'),
        ('otros', 'Otros'),
    )
    poa = models.ForeignKey(
        to= POA,
        verbose_name= 'POA',
        on_delete=models.CASCADE,
        related_name='expenses',
        help_text='POA al cual pertenece el gasto.',  
    )
    expense_type = models.CharField(
        verbose_name= 'tipo',
        max_length= 32,
        choices= EXPENSE_TYPES,
        default='otros',
        help_text= 'Tipo del gasto.', 
    )  
    description = models.CharField(
        verbose_name= 'descripción',
        max_length= 256,
        help_text= 'Descripción del gasto.'
    )
    value = models.FloatField(
        verbose_name=f'valor (Bs.)',
        help_text= f'Valor en bolivianos del gasto.'
    )
    class Meta:
        verbose_name = 'Gasto POA'
        verbose_name_plural = 'Gastos POAs'
        ordering = ['poa', 'id',]

    def __str__(self):
        return f'{self.poa} ({self.id})'


class Investment(models.Model):
    '''
    Modelo representando una inversión presupuestada de un POA.
    '''
    poa = models.ForeignKey(
        to= POA,
        verbose_name= 'POA',
        on_delete=models.CASCADE,
        related_name='investments',
        help_text='POA al cual pertenece la inversión.',  
    )
    description = models.CharField(
        verbose_name= 'descripción',
        max_length= 256,
        help_text= 'Descripción de la inversión.'
    )
    value = models.FloatField(
        verbose_name=f'valor (Bs.)',
        help_text= f'Valor en bolivianos de la inversión.'
    )
    class Meta:
        verbose_name = 'Inversión POA'
        verbose_name_plural = 'Inversiones POAs'
        ordering = ['poa', 'id',]

    def __str__(self):
        return f'{self.poa} ({self.id})'


class Goal(models.Model):
    '''
    Modelo representando una meta de expansión de un POA.
    '''
    poa = models.ForeignKey(
        to= POA,
        verbose_name= 'POA',
        on_delete=models.CASCADE,
        related_name='goals',
        help_text='POA al cual pertenece la meta.',  
    )
    description = models.CharField(
        verbose_name= 'descripción',
        max_length= 256,
        help_text= 'Descripción de la meta.'
    )
    
    value = models.FloatField(
        verbose_name=f'valor',
        help_text= f'Valor de la meta.'
    )
    val_description = models.CharField(
        verbose_name='descripción del valor',
        max_length=64,
        help_text='Descripción de lo que representa el valor de la meta (ejemplo: más de X conexiones nuevas de agua potable o simplemente ">").',
        blank=True, null=True,
    )
    unit = models.CharField(
        verbose_name= 'unidad',
        max_length= 64,
        help_text= 'Unidad de la meta.'
    )
    class Meta:
        verbose_name = 'Meta de expansión POA'
        verbose_name_plural = 'Metas de expansión POAs'
        ordering = ['poa', 'id',]

    def __str__(self):
        return f'{self.poa} ({self.id})'



class Plan(models.Model):
    '''
    Modelo representando un plan de desarrollo quinquenal (PDQ) o un plan transitorio de desarrollo sostenible (PTDS).
    '''
    PLAN_TYPES = (
        ('pdq', 'PDQ'),
        ('ptds', 'PTDS'),
    )

    epsa = models.ForeignKey(
        to=EPSA,
        verbose_name='EPSA',
        on_delete=models.CASCADE,
        related_name='ptds',
        help_text='EPSA que reporta el PTDS'
    )
    year = models.IntegerField(
        verbose_name='Año Inicial',
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900)],
        help_text='Primer año de vigencia del PTDS'
    )
    plan_type = models.CharField(
        verbose_name= 'tipo de plan',
        max_length= 8,
        choices= PLAN_TYPES,
        default='pdq',
        help_text= 'Tipo del plan (PDQ o PTDS).', 
    )  
    class Meta:
        unique_together = ('epsa','year')
        verbose_name = 'PDQ/PTDS'
        verbose_name_plural = 'PDQs/PTDS'
        ordering = ['epsa__code','year',]

    def __str__(self):
        return f'{self.epsa}-{self.year}-{self.plan_type}'
    def get_category(self):
        return self.epsa.category
    get_category.short_description = 'categoría'
    def get_state(self):
        return state_code_to_name[self.epsa.state]
    get_state.short_description = 'departamento'


class PlanGoal(models.Model):
    '''
    Modelo representando una meta de expansión de un PDQ o PTDS.
    '''
    plan = models.ForeignKey(
        to= Plan,
        verbose_name= 'PDQ/PTDS',
        on_delete=models.CASCADE,
        related_name='goals',
        help_text='PDQ/PTDS al cual pertenece la meta.',  
    )
    year = models.IntegerField(
        verbose_name='año',
        default=datetime.datetime.now().year,
        validators=[MinValueValidator(1900)],
        help_text='año del plan'
    )
    description = models.CharField(
        verbose_name= 'descripción',
        max_length= 256,
        help_text= 'Descripción de la meta.'
    )
    value = models.FloatField(
        verbose_name=f'valor',
        help_text= f'Valor de la meta.'
    )
    val_description = models.CharField(
        verbose_name='descripción del valor',
        max_length=64,
        help_text='Descripción de lo que representa el valor de la meta (ejemplo: más de X conexiones nuevas de agua potable o simplemente ">").',
        blank=True, null=True,
    )
    unit = models.CharField(
        verbose_name= 'unidad',
        max_length= 64,
        help_text= 'Unidad de la meta.'
    )
    class Meta:
        verbose_name = 'Meta de expansión PDQ/PTDS'
        verbose_name_plural = 'Metas de expansión PDQ/PTDS'
        ordering = ['plan', 'id',]

    def __str__(self):
        return f'{self.plan} ({self.id})'



