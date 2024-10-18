from rest_framework import serializers

from admin_account.project.serializers import AdminProjectsSerializer
from authen.serializers import UserInformationContractorSerializer, UserInformationCustomerSerializer, UserInformationSerializer
from prescription.models import TypeOfViolation, Prescriptions, PrescriptionsImage, PrescriptionsComment


class TypeOFViolationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfViolation
        fields = ['id', 'name']


class PrescriptionsImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrescriptionsImage
        fields = ['id', 'image']


class PrescriptionsCommentSerializer(serializers.ModelSerializer):
    owner = UserInformationSerializer(read_only=True)

    class Meta:
        model = PrescriptionsComment
        fields = ['id', 'comment', 'owner']


class CustomerPrescriptionsSerializers(serializers.ModelSerializer):
    project = AdminProjectsSerializer(read_only=True)
    owner = UserInformationCustomerSerializer(read_only=True)
    contractor = UserInformationContractorSerializer(many=True)
    type_violation = TypeOFViolationSerializer(many=True)
    prescription_image = PrescriptionsImageSerializer(many=True)
    prescription_comment = PrescriptionsCommentSerializer(many=True)

    class Meta:
        model = Prescriptions
        fields = ['id', 'project', 'contractor', 'type_violation', 'deadline', 'owner', 'prescription_image', 'prescription_comment', 'create_at']


class CustomerPrescriptionSerializers(serializers.ModelSerializer):
    respost_comment = PrescriptionsCommentSerializer(many=True, required=False)

    class Meta:
        model = Prescriptions
        fields = ['id', 'project', 'contractor', 'type_violation', 'deadline', 'owner', 'prescription_image', 'prescription_comment', 'create_at']

    def create(self, validated_data):
        owner = self.context.get('owner')

        if owner.report_processing:
            raise serializers.ValidationError({"error": "Разрешения на создание предписаний нет."})


        prescription_comment = validated_data.pop('prescription_comment', None)
        
        # ReportsName ni yaratish
        reports_name = Prescriptions.objects.create(**validated_data)

        return reports_name