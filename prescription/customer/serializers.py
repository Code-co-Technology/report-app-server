import json
from rest_framework import serializers

from authen.models import CustomUser
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
    type_violation = TypeOFViolationSerializer(many=True)
    prescription_image = PrescriptionsImageSerializer(many=True)
    prescription_comment = PrescriptionsCommentSerializer(many=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Prescriptions
        fields = ['id', 'status', 'project', 'type_violation', 'deadline', 'owner', 'prescription_image', 'prescription_comment', 'create_at']


class CustomerPrescriptionSerializers(serializers.ModelSerializer):
    prescription_image = serializers.ListField(child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True, required=False)
    prescription_comment = serializers.ListField(child = serializers.CharField(max_length = 1000000),
        write_only=True, required=False)
    type_violation = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Prescriptions
        fields = ['id', 'project', 'type_violation', 'deadline', 'owner', 'prescription_image', 'prescription_comment', 'create_at']

    def create(self, validated_data):
        owner = self.context.get('owner')

        if owner.report_processing:
            raise serializers.ValidationError({"error": "Разрешения на создание предписаний нет."})

        # Pop prescription comment and images data
        prescription_comment = validated_data.pop('prescription_comment', [])
        images_data = validated_data.pop('prescription_image', [])

        type_violation_data = json.loads(validated_data.pop('type_violation', '[]'))

        # Create the prescription object
        prescription = Prescriptions.objects.create(**validated_data)
        prescription.owner = owner

        # Set valid type violations
        if type_violation_data:
            valid_violations = TypeOfViolation.objects.filter(id__in=type_violation_data)
            if len(valid_violations) != len(type_violation_data):
                raise serializers.ValidationError('Some violation IDs are invalid.')
            prescription.type_violation.set(valid_violations)

        # Save prescription after setting relations
        prescription.save()

        # Create prescription comments if provided (assuming comments are strings)
        for comment_text in prescription_comment:
            PrescriptionsComment.objects.create(prescription=prescription, owner=owner, comment=comment_text)

        # Create prescription images if provided
        if images_data:
            PrescriptionsImage.objects.bulk_create([
                PrescriptionsImage(prescription=prescription, image=image_data)
                for image_data in images_data
            ])

        return prescription
    
    def update(self, instance, validated_data):
        # Extracting nested data
        images_data = validated_data.pop('prescription_image', [])
        prescription_comment = validated_data.pop('prescription_comment', None)
        # Update instance fields
        instance.project = validated_data.get('project', instance.project)
        instance.deadline = validated_data.get('deadline', instance.deadline)
        instance.contractor = validated_data.get('contractor', instance.contractor)
        

        type_violation_data = validated_data.pop('type_violation', None)
        if type_violation_data:
            type_violation_data = json.loads(type_violation_data)

        # Process contractors only if provided
        if type_violation_data:
            valid_contractors = []
            for type_violation_data_id in type_violation_data:
                try:
                    version_obj = TypeOfViolation.objects.get(id=type_violation_data_id)
                    valid_contractors.append(version_obj)  # Collect valid contractor objects
                except TypeOfViolation.DoesNotExist:
                    raise serializers.ValidationError(f'Contractor with id {type_violation_data_id} does not exist.')

            # Update contractors
            instance.type_violation.set(valid_contractors)

        instance.save()

        # Update ProjectImage
        if images_data:
            # Clear existing images if necessary
            PrescriptionsImage.objects.filter(prescription=instance).delete()  # Optional: Uncomment if you want to replace images
            for image_data in images_data:
                PrescriptionsImage.objects.create(prescription=instance, image=image_data)
        
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
