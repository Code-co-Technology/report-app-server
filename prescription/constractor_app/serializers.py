from rest_framework import serializers

from authen.serializers import UserInformationSerializer, UserInformationContractorSerializer
from admin_account.project.serializers import AdminProjectsSerializer
from prescription.models import Prescriptions, PrescriptionsComment, PrescriptionContractor
from prescription.customer.serializers import TypeOFViolationSerializer, PrescriptionsImageSerializer, PrescriptionsCommentSerializer


class ConstractorPrescriptionSerializer(serializers.ModelSerializer):
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


class ConstractorPrescriptionsSerializer(serializers.ModelSerializer):
    prescription = ConstractorPrescriptionSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')
    user = serializers.SerializerMethodField()
    contractor = UserInformationContractorSerializer(read_only=True)

    class Meta:
        model = PrescriptionContractor
        fields = ['id', 'prescription', 'contractor', 'user', 'status', 'create_at']

    def get_user(self, obj):
        if obj.user:
            return {
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
            }
        return None 


class ConstractorPrescriptionsUpddateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PrescriptionContractor
        fields = ['id', 'prescription', 'user', 'status']

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        # Update instance fields
        instance.save()
        return instance


class ContractorsPrescriptionSerializers(serializers.ModelSerializer):
    prescription_comment = serializers.ListField(
        child = serializers.CharField(max_length = 1000000),
        write_only=True, required=False
    )

    class Meta:
        model = Prescriptions
        fields = ['id', 'prescription_comment']
    
    def update(self, instance, validated_data):
        prescription_comment = validated_data.pop('prescription_comment', None)
        # Update instance fields
        instance.save()

        if prescription_comment:
            existing_comments = {comment.id: comment for comment in instance.respost_comment.all()}
            owner = self.context.get('owner')

            for comment_data_item in prescription_comment:
                comment_id = comment_data_item.get('id', None)

                if comment_id and comment_id in existing_comments:
                    # Agar komment mavjud bo'lsa, uni yangilaymiz
                    comment = existing_comments[comment_id]
                    for attr, value in comment_data_item.items():
                        setattr(comment, attr, value)
                    comment.owner = owner
                    comment.save()
                else:
                    # Agar komment yangi bo'lsa, uni yaratamiz
                    PrescriptionsComment.objects.create(prescription=instance, owner=owner, **comment_data_item)

        return instance
