from rest_framework import serializers
from drf_queryfields import QueryFieldsMixin
from performance.models import EPSA, Variable, Indicator, VariableReport, IndicatorMeasurement

class EPSASerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = EPSA
        fields = '__all__'

class VariableSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Variable
        fields = '__all__'

class IndicatorSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    # formula = serializers.JSONField()
    class Meta:
        model = Indicator
        fields = '__all__'

class VariableReportSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = VariableReport
        fields = '__all__'

class IndicatorMeasurementSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = IndicatorMeasurement
        fields = '__all__'