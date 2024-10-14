from rest_framework import serializers

from admin_account.models import ProjectStatus, Project, ProjectImage, ProjectSmeta


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

    class Meta:
        model = Project
        fields = ['id', 'address', 'opening_date', 'submission_deadline', 'contractor', 'status', 'project_image', 'project_files']


class AdminCreateProjectSerializer(serializers.ModelSerializer):
    project_image = AdminProjectImagesSerializer(many=True, required=False) # Optional
    project_files = AdminProjectFilesSerializer(many=True, required=False) # Optional

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

        # Get the default status
        status_project = ProjectStatus.objects.get(name='В работе')

        # Create the project
        project = Project.objects.create(**validated_data)
        project.status = status_project
        project.owner = self.context.get('owner')
        project.save()

        # Handle ProjectImage creation
        for image_data in images_data:
            ProjectImage.objects.create(project=project, **image_data)

        # Handle ProjectSmeta creation
        for file_data in files_data:
            ProjectSmeta.objects.create(project=project, **file_data)

        return project


class AdminUpdateProjectSerializer(serializers.ModelSerializer):
    project_image = AdminProjectImagesSerializer(many=True, required=False) # Optional
    project_files = AdminProjectFilesSerializer(many=True, required=False) # Optional

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
        images_data = validated_data.pop('project_image', [])
        files_data = validated_data.pop('project_files', [])
        
        # Yangilanishni amalga oshiring
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        
        # Agar yangi rasm yoki fayl kelgan bo'lsa, yangilash
        if images_data:
            instance.project_image.all().delete()  # Eski rasmlarni o'chirish
            for image in images_data:
                ProjectImage.objects.create(project=instance, **image)
        
        if files_data:
            instance.project_files.all().delete()  # Eski fayllarni o'chirish
            for file in files_data:
                ProjectFile.objects.create(project=instance, **file)

        return instance