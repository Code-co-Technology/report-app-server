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
    prescription_image = serializers.ListField(child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True, required=False)
    prescription_comment = PrescriptionsCommentSerializer(many=True, required=False)

    class Meta:
        model = Prescriptions
        fields = ['id', 'project', 'contractor', 'type_violation', 'deadline', 'owner', 'prescription_image', 'prescription_comment', 'create_at']

    def create(self, validated_data):
        owner = self.context.get('owner')

        if owner.report_processing:
            raise serializers.ValidationError({"error": "Разрешения на создание предписаний нет."})

        prescription_comment = validated_data.pop('prescription_comment', None)
        images_data = validated_data.pop('prescription_image', [])

        respost = Prescriptions.objects.create(**validated_data)
        respost.owner = owner
        respost.save()

        # Comment create
        for respost_data in prescription_comment:
            PrescriptionsComment.objects.create(prescription=respost, owner=owner, **respost_data)
        
        for image_data in images_data:
            PrescriptionsImage.objects.create(prescription=respost, image=image_data)

        return respost