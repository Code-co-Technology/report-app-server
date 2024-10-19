import json
from rest_framework import serializers

from admin_account.models import ProjectStatus, Project, ProjectImage, ProjectSmeta
from authen.serializers import UserInformationContractorSerializer
from authen.models import CustomUser


class ProjectStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectStatus
        fields = ['id', 'name']


class AdminProjectImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectImage
        fields = ['id', 'image']


class AdminProjectFilesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSmeta
        fields = ['id', 'files']


class AdminProjectsSerializer(serializers.ModelSerializer):
    project_image = AdminProjectImagesSerializer(many=True, read_only=True)
    project_files = AdminProjectFilesSerializer(many=True, read_only=True)
    contractor = UserInformationContractorSerializer(many=True)
    status = ProjectStatusSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'address', 'opening_date', 'submission_deadline', 'contractor', 'status', 'project_image', 'project_files']


class AdminCreateProjectSerializer(serializers.ModelSerializer):
    project_image = serializers.ListField(child = serializers.ImageField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True, required=False) # Optional
    project_files = serializers.ListField(child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True, required=False) # Optional
    contractor = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'address', 'opening_date', 'submission_deadline', 'contractor', 'project_image', 'project_files']
        # The list of required fields will automatically have required=True
        extra_kwargs = {
            'address': {'required': True},
            'opening_date': {'required': True},
            'submission_deadline': {'required': True}
        }

    def create(self, validated_data):
        # Extracting nested data
        images_data = validated_data.pop('project_image', [])
        files_data = validated_data.pop('project_files', [])

        # Handle contractors_data as optional
        contractors_data = validated_data.pop('contractor', [])
        if contractors_data:
            contractors_data = json.loads(contractors_data) 
    
        # Get the default status
        status_project = ProjectStatus.objects.get(name='В работе')

        # Create the project
        project = Project.objects.create(**validated_data)
        project.status = status_project
        project.owner = self.context.get('owner')
        project.contractor.set(contractors_data)

        # Process contractors only if provided
        if contractors_data:
        # Ensure contractors_data is a list of valid user IDs
            valid_contractors = []
            for contractor_id in contractors_data:
                try:
                    version_obj = CustomUser.objects.get(id=contractor_id)
                    valid_contractors.append(version_obj)  # Collect valid contractor objects
                except CustomUser.DoesNotExist:
                    raise serializers.ValidationError(f'Contractor with id {contractor_id} does not exist.')

            # Set the valid contractors to the project's contractor field
            project.contractor.set(valid_contractors)

        project.save()

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
        fields = ['id', 'address', 'opening_date', 'submission_deadline', 'contractor', 'project_image', 'project_files']
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

        # Handle contractors_data as optional
        contractors_data = validated_data.pop('contractor', None)
        if contractors_data:
            contractors_data = json.loads(contractors_data)

        # Update instance fields
        instance.address = validated_data.get('address', instance.address)
        instance.opening_date = validated_data.get('opening_date', instance.opening_date)
        instance.submission_deadline = validated_data.get('submission_deadline', instance.submission_deadline)

        # Process contractors only if provided
        if contractors_data:
            valid_contractors = []
            for contractor_id in contractors_data:
                try:
                    version_obj = CustomUser.objects.get(id=contractor_id)
                    valid_contractors.append(version_obj)  # Collect valid contractor objects
                except CustomUser.DoesNotExist:
                    raise serializers.ValidationError(f'Contractor with id {contractor_id} does not exist.')

            # Update contractors
            instance.contractor.set(valid_contractors)

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

        return instance