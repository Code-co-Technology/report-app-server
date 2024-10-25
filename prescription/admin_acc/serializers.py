from rest_framework import serializers

from authen.serializers import UserInformationContractorSerializer
from prescription.models import Prescriptions, PrescriptionsComment, PrescriptionContractor
from prescription.customer.serializers import PrescriptionsCommentSerializer, PrescriptionsImageSerializer, TypeOFViolationSerializer


class AdminPrescriptionsSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    prescription_image = PrescriptionsImageSerializer(many=True)
    prescription_comment = PrescriptionsCommentSerializer(many=True)
    type_violation = TypeOFViolationSerializer(many=True)

    class Meta:
        model = Prescriptions
        fields = ['id', 'type_violation', 'project', 'deadline', 'prescription_image', 'prescription_comment', 'owner']
    
    def get_project(self, obj):
        return {
            'create_at': obj.project.opening_date,
        }
    
    def get_owner(self, obj):
        full_name = obj.owner.first_name + ' ' + obj.owner.last_name
        return {
            'name': full_name
        }


class AdminPrescriptionsUserSerializer(serializers.ModelSerializer):
    prescription = AdminPrescriptionsSerializer(read_only=True)
    contractor = UserInformationContractorSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = PrescriptionContractor
        fields = ['id', 'prescription', 'contractor', 'status']


class AdminPrescriptionSerializers(serializers.ModelSerializer):

    class Meta:
        model = PrescriptionContractor
        fields = ['id', 'status']
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)

        return instance
