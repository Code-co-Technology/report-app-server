from rest_framework import serializers

from authen.serializers import UserInformationContractorSerializer
from prescription.models import Prescriptions, PrescriptionsComment, PrescriptionContractor
from prescription.customer.serializers import PrescriptionsImageSerializer, PrescriptionsCommentSerializer, TypeOFViolationSerializer


class UserPrescriptionSerializer(serializers.ModelSerializer):
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
        if obj.owner:
            full_name = obj.owner.first_name + ' ' + obj.owner.last_name
            return {
                'name': full_name
            }
        return None

class UserPrescriptionsSerializer(serializers.ModelSerializer):
    prescription = UserPrescriptionSerializer(read_only=True)
    contractor = UserInformationContractorSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')
    user = serializers.SerializerMethodField()

    class Meta:
        model = PrescriptionContractor
        fields = ['id', 'prescription', 'contractor', 'user', 'status']

    def get_user(self,obj):
        if obj.user:
            return {
                "full_name": obj.user.first_name + ' ' + obj.user.last_name
            }
        return None



class UserPrescriptionsUpddateSerializer(serializers.ModelSerializer):
    prescription_comment = serializers.ListField(child = serializers.CharField(max_length = 1000000),
        write_only=True, required=False)
    prescription = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = PrescriptionContractor
        fields = ['id', 'prescription', 'prescription_comment']

    def update(self, instance, validated_data):

        prescription_comment = validated_data.pop('prescription_comment', [])
        prescription = validated_data.pop('prescription', None)
        owner = self.context.get('owner')
        
        if prescription:
            try:
                prescription = Prescriptions.objects.get(id=prescription)
            except Prescriptions.DoesNotExist:
                raise serializers.ValidationError("The provided prescription does not exist.")
        else:
            prescription = None
        for comment_text in prescription_comment:
            PrescriptionsComment.objects.create(prescription=prescription, owner=owner, comment=comment_text)
        instance.save()
        return instance