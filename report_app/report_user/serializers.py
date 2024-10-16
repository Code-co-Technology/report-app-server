from rest_framework import serializers

from report_app.reports.serializers import BobSerializers, TypeOfWorkSerializer
from report_app.models import ReportsName, Reports, RespostComment



class ResportCreateSerializer(serializers.ModelSerializer):

     class Meta:
          model = Reports
          fields = [
               'id', 
               'bob', 
               'type_work', 
               'position',
               'quantity',
               'frame',
               'floor',
               'mark',
               'axles',
               'premises',
               'completions',
               'files',
               'create_at'
          ]


class ReportsNameCreateSerializer(serializers.ModelSerializer):
    resposts = ResportCreateSerializer(many=True)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'respost_comment', 'constructor_accepted', 'resposts', 'user', 'create_at']

    def create(self, validated_data):
        # resposts ma'lumotlarini validated_data dan ajratib oling
        resposts_data = validated_data.pop('resposts')
        
        # ReportsName ni yaratish
        reports_name = ReportsName.objects.create(**validated_data)
        
        # Foydalanuvchini context orqali bog'lab qo'shish
        reports_name.user = self.context.get('user')
        reports_name.save()

        # Har bir respost uchun alohida Reports obyektlarini yaratish
        for respost_data in resposts_data:
            Reports.objects.create(reports_name=reports_name, **respost_data)

        return reports_name

    def update(self, instance, validated_data):
        # resposts ma'lumotlarini validated_data'dan ajratish
        resposts_data = validated_data.pop('resposts')

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.respost_comment = validated_data.get('respost_comment', instance.respost_comment)
        instance.constructor_accepted = validated_data.get('constructor_accepted', instance.constructor_accepted)
        instance.user = self.context.get('user', instance.user)
        instance.save()

        # Mavjud `resposts` obyektlarini o'chirish
        instance.resposts.all().delete()

        # Yangilangan `resposts` obyektlarini yaratish
        for respost_data in resposts_data:
            Reports.objects.create(reports_name=instance, **respost_data)

        return instance