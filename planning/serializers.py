from rest_framework import serializers
from planning import models
from drf_queryfields import QueryFieldsMixin


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Income
        exclude = ('id','poa')
class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Expense
        exclude = ('id','poa')
class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Investment
        exclude = ('id','poa')
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Goal
        exclude = ('id','poa')


class POASerializer(QueryFieldsMixin, serializers.ModelSerializer):
    incomes = IncomeSerializer(many=True, required=False)
    expenses = ExpenseSerializer(many=True, required=False)
    investments = InvestmentSerializer(many=True, required=False)
    goals = GoalSerializer(many=True, required=False)

    class Meta:
        model = models.POA
        fields = '__all__'

    def create(self, validated_data):
        objects_types = ['incomes','expenses','investments','goals',]
        objects_models = [models.Income, models.Expense, models.Investment, models.Goal]
        objects_data = {}

        for obj_type in objects_types:
            objects_data[obj_type] = validated_data.pop(obj_type, None)

        poa = models.POA.objects.create(**validated_data)

        for obj_type, obj_model in zip(objects_types, objects_models):
            objs_data = objects_data[obj_type]
            if objs_data:
                for obj_data in objs_data:
                    obj_model.objects.create(poa=poa, **obj_data)
        return poa

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