import json
from rest_framework import serializers

from admin_account.models import ProjectStatus, Project, ProjectImage, ProjectSmeta
from authen.serializers import UserInformationContractorSerializer, UserInformationCustomerSerializer
from authen.models import CustomUser
from prescription.models import Prescriptions, PrescriptionContractor

class ProjectStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectStatus
        fields = ['id', 'name']


class AdminProjectImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectImage
        fields = ['id', 'image']


class AdminProjectImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)

    class Meta:
        model = ProjectImage
        fields = ['id', 'image']
    

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        
        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)

        instance.save()
        return instance


class AdminProjectFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSmeta
        fields = ['id', 'files']


class AdminProjectFileSerializer(serializers.ModelSerializer):
    files = serializers.FileField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)

    class Meta:
        model = ProjectSmeta
        fields = ['id', 'files']
    
    def update(self, instance, validated_data):
        instance.files = validated_data.get('files', instance.files)

        if instance.files == None:
            instance.files = self.context.get("files")
        else:
            instance.files = validated_data.get("files", instance.files)

        instance.save()
        return instance


class PrescriptionContractorSerializer(serializers.ModelSerializer):
    contractor = UserInformationContractorSerializer(read_only=True)  # 'contractor' ga tegishli bo'lgan serializer

    class Meta:
        model = PrescriptionContractor
        fields = ['id', 'contractor', 'status']


class CustomerPrescriptionsProjectSerializers(serializers.ModelSerializer):
    contractor_statuses = PrescriptionContractorSerializer(many=True)
    owner = UserInformationContractorSerializer(read_only=True) 

    class Meta:
        model = Prescriptions
        fields = ['id', 'deadline', 'contractor_statuses', 'owner']


class AdminProjectsSerializer(serializers.ModelSerializer):
    project_image = AdminProjectImagesSerializer(many=True, read_only=True)
    project_files = AdminProjectFilesSerializer(many=True, read_only=True)
    status = ProjectStatusSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'address', 'opening_date', 'submission_deadline', 'status', 'project_image', 'project_files']


class AdminCreateProjectSerializer(serializers.ModelSerializer):
    project_image = serializers.ListField(child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True, required=False) # Optional
    project_files = serializers.ListField(child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True, required=False) # Optional
    contractor = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'address', 'opening_date', 'submission_deadline', 'project_image', 'project_files', 'contractor']
        # The list of required fields will automatically have required=True
        extra_kwargs = {
            'address': {'required': True},
            'opening_date': {'required': True},
            'submission_deadline': {'required': True}
        }

    def create(self, validated_data):
        images_data = validated_data.pop('project_image', [])
        files_data = validated_data.pop('project_files', [])

        contractors_data = validated_data.pop('contractor', [])
        if contractors_data:
            contractors_data = json.loads(contractors_data) 
        deadline = validated_data.get('submission_deadline')
        status_project = ProjectStatus.objects.get(name='В обработке')
        project = Project.objects.create(**validated_data)
        project.status = status_project
        project.owner = self.context.get('owner')
        project.save()

        if contractors_data:
            presc = Prescriptions.objects.create(
                project=project,
                deadline=deadline,
                status=1,
                owner=self.context.get('owner')
            )
            for contractor_id in contractors_data:
                contractor = CustomUser.objects.get(id=contractor_id)  # Get the CustomUser instance
                PrescriptionContractor.objects.create(
                    prescription=presc,
                    contractor=contractor,  # Now contractor is a CustomUser instance
                    status=1  # Default status for contractors
                )
        # Handle ProjectImage creation
        for image_data in images_data:
            ProjectImage.objects.create(project=project, image=image_data)

        # Handle ProjectSmeta creation
        for file_data in files_data:
            ProjectSmeta.objects.create(project=project, files=file_data)

        return project


class AdminUpdateProjectSerializer(serializers.ModelSerializer):
    project_image = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )  # Optional
    project_files = serializers.ListField(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )  # Optional
    contractor = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'address', 'opening_date', 'contractor', 'submission_deadline', 'project_image', 'project_files']
        # The list of required fields will automatically have required=True
        extra_kwargs = {
            'address': {'required': True},
            'opening_date': {'required': True},
            'submission_deadline': {'required': True}
        }

    def update(self, instance, validated_data):
        # Extracting nested data
        images_data = validated_data.pop('project_image', [])
        files_data = validated_data.pop('project_files', [])

        # Update instance fields
        instance.address = validated_data.get('address', instance.address)
        instance.opening_date = validated_data.get('opening_date', instance.opening_date)
        new_submission_deadline = validated_data.get('submission_deadline', instance.submission_deadline)

        instance.save()

        # Update ProjectImage
        if images_data:
            # Clear existing images if necessary
            ProjectImage.objects.filter(project=instance).delete()  # Optional: Uncomment if you want to replace images
            for image_data in images_data:
                ProjectImage.objects.create(project=instance, image=image_data)

        # Update ProjectSmeta
        if files_data:
            # Clear existing files if necessary
            ProjectSmeta.objects.filter(project=instance).delete()  # Optional: Uncomment if you want to replace files
            for file_data in files_data:
                ProjectSmeta.objects.create(project=instance, files=file_data)
        
        contractors_data = validated_data.pop('contractor', None)
    
        # If either contractors or submission_deadline is updated
        if contractors_data or new_submission_deadline != instance.submission_deadline:
            if contractors_data:
                contractors_data = json.loads(contractors_data)

            # Clear existing contractor relationships only if contractors_data has changed
            PrescriptionContractor.objects.filter(prescription__project=instance).delete()

            # Check if we need to create or update Prescriptions instance
            presc = Prescriptions.objects.filter(project=instance).first()
            if presc is None:
                # If no existing prescription, create a new one
                presc = Prescriptions.objects.create(
                    project=instance,
                    deadline=new_submission_deadline,
                    status=1,
                    owner=self.context.get('owner')
                )
            else:
                # Update existing prescription's deadline if it has changed
                if new_submission_deadline != instance.submission_deadline:
                    presc.deadline = new_submission_deadline
                    presc.save()

            # Now handle contractor assignments if contractors_data is provided
            if contractors_data:
                for contractor_id in contractors_data:
                    contractor = CustomUser.objects.get(id=contractor_id)
                    PrescriptionContractor.objects.create(
                        prescription=presc,
                        contractor=contractor,
                        status=1  # Default status for contractors
                    )

        # Update submission deadline for the project instance if changed
        if new_submission_deadline != instance.submission_deadline:
            instance.submission_deadline = new_submission_deadline
            instance.save()

        return instance