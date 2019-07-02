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
    epsa = serializers.CharField(allow_blank=True,required=False)
    class Meta:
        model = VariableReport
        fields = '__all__'
    def create(self, validated_data):
        epsa_code = validated_data.pop('epsa',None)

        if epsa_code:
            epsa_tuple = EPSA.objects.get_or_create(code=epsa_code)
            report = VariableReport.objects.create(epsa=epsa_tuple[0], **validated_data)
        else:
            report = VariableReport.objects.create(**validated_data)

        return report

class IndicatorMeasurementSerializer(QueryFieldsMixin, serializers.ModelSerializer):
    epsa = serializers.CharField(allow_blank=True,required=False)

    class Meta:
        model = IndicatorMeasurement
        fields = '__all__'
    
    def create(self, validated_data):
        epsa_code = validated_data.pop('epsa',None)

        if epsa_code:
            epsa_tuple = EPSA.objects.get_or_create(code=epsa_code)
            measurement = IndicatorMeasurement.objects.create(epsa=epsa_tuple[0], **validated_data)
        else:
            measurement = IndicatorMeasurement.objects.create(**validated_data)

        return measurement
    

