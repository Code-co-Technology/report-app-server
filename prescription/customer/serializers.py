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
        fields = ['id', 'comment', 'onwer']


class CustomerPrescriptionsSerializers(serializers.ModelSerializer):
    project = AdminProjectsSerializer(read_only=True)
    owner = UserInformationCustomerSerializer(read_only=True)
    contractor = UserInformationContractorSerializer(many=True)
    type_violation = TypeOFViolationSerializer(many=True)
    prescription_image = PrescriptionsImageSerializer(many=True)
    prescription_comment = PrescriptionsCommentSerializer(many=True)

    class Meta:
        model = Prescriptions
        fields = ['id', 'project', 'contractor', 'type_violation', 'deadline', 'owner', 'create_at']
