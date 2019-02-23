from django.contrib import admin
from planning import models

class IncomeInline(admin.TabularInline):
    model = models.Income
    verbose_name = 'Ingreso'
    verbose_name_plural = 'Ingresos Presupuestados'

class ExpenseInline(admin.TabularInline):
    model = models.Expense
    verbose_name = 'Gasto'
    verbose_name_plural = 'Gastos Presupuestados'

class InvestmentInline(admin.TabularInline):
    model = models.Investment
    verbose_name = 'Inversión'
    verbose_name_plural = 'Inversiones Presupuestadas'

class GoalInline(admin.TabularInline):
    model = models.Goal
    verbose_name = 'Meta de expansión'
    verbose_name_plural = 'Metas de expansión'

class PlanGoalInline(admin.TabularInline):
    model = models.PlanGoal
    verbose_name = 'Meta'
    verbose_name_plural = 'Metas'


@admin.register(models.POA)
class POAModelAdmin(admin.ModelAdmin):
    view_on_site = False

    inlines = [
        IncomeInline,
        ExpenseInline,
        InvestmentInline,
        GoalInline
    ]
    
    list_filter = ('epsa__category', 'epsa__state','year')
    search_fields = ['epsa', 'epsa__name', 'epsa__state',]
    list_display = ('epsa', 'year', 'order', 'get_category', 'get_state',)

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Planificación: POAs'}
        return super(POAModelAdmin, self).changelist_view(request, extra_context=extra_context)

@admin.register(models.Plan)
class PlanModelAdmin(admin.ModelAdmin):
    view_on_site = False
    inlines = [
        PlanGoalInline,
    ]
    
    list_display = ('epsa', 'year', 'plan_type', 'get_category', 'get_state',)
    list_filter = ('epsa__category', 'epsa__state','year')
    search_fields = ['epsa', 'epsa__name', 'epsa__state',]

    def changelist_view(self, request, extra_context=None):
        extra_context = {'title': 'AAPS - Planificación: PDQs/PTDS'}
        return super(PlanModelAdmin, self).changelist_view(request, extra_context=extra_context)


