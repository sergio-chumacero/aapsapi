from rest_framework import serializers
from planning import models
from performance.models import EPSA
from drf_queryfields import QueryFieldsMixin


class CoopExpenseSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.CoopExpense
        exclude = ('id','poa',)

class MuniExpenseSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = models.MuniExpense
        exclude = ('id','poa',)


class POASerializer(QueryFieldsMixin, serializers.ModelSerializer):
    coop_expense = CoopExpenseSerializer(required=False)
    muni_expense = MuniExpenseSerializer(required=False)

    class Meta:
        model = models.POA
        fields = '__all__'

    def create(self, validated_data):
        epsa_code = validated_data.pop('epsa',None)
        coop_expense = validated_data.pop('coop_expense', None)
        muni_expense = validated_data.pop('muni_expense', None)

        if epsa_code:
            epsa_tuple = EPSA.objects.get_or_create(code=epsa_code)
            poa = models.POA.objects.create(epsa=epsa_tuple[0], **validated_data)
        else:
            poa = models.SARH.objects.create(**validated_data)

        if coop_expense is not None:
            models.CoopExpense.objects.create(poa=poa,**coop_expense)
        if muni_expense is not None:
            models.MuniExpense.objects.create(poa=poa,**muni_expense)

        return poa

    # def create(self, validated_data):
    #     objects_types = ['incomes','expenses','investments','goals',]
    #     objects_models = [models.Income, models.Expense, models.Investment, models.Goal]
    #     objects_data = {}

    #     for obj_type in objects_types:
    #         objects_data[obj_type] = validated_data.pop(obj_type, None)

    #     poa = models.POA.objects.create(**validated_data)

    #     for obj_type, obj_model in zip(objects_types, objects_models):
    #         objs_data = objects_data[obj_type]
    #         if objs_data:
    #             for obj_data in objs_data:
    #                 obj_model.objects.create(poa=poa, **obj_data)
        # return poa

class PlanGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PlanGoal
        exclude = ('id','plan',)

class PlanSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    goals = PlanGoalSerializer(many=True, required=False)
    
    class Meta:
        model = models.Plan
        fields = '__all__'
    
    def create(self, validated_data):
        goals_data = validated_data.pop('goals', None)
        plan = models.Plan.objects.create(**validated_data)

        if goals_data:
            for goal_data in goals_data:
                models.PlanGoal.objects.create(plan=plan, **goal_data)
        return plan                