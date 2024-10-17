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
    resposts = ResportCreateSerializer(many=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'status_user', 'resposts', 'user', 'create_at']

    def create(self, validated_data):
        # resposts ma'lumotlarini validated_data dan ajratib oling
        resposts_data = validated_data.pop('resposts')
        
        # ReportsName ni yaratish
        reports_name = ReportsName.objects.create(**validated_data)
        
        # Foydalanuvchini context orqali bog'lab qo'shish
        reports_name.user = self.context.get('user')
        reports_name.status_user = 1
        reports_name.status_contractor = 1
        reports_name.save()

        # Har bir respost uchun alohida Reports obyektlarini yaratish
        for respost_data in resposts_data:
            Reports.objects.create(reports_name=reports_name, **respost_data)

        return reports_name

    def update(self, instance, validated_data):
        # resposts ma'lumotlarini validated_data'dan ajratish
        resposts_data = validated_data.pop('resposts', None)

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        if resposts_data:
            # Mavjud resposts'larni id bo'yicha olamiz
            existing_resposts = {respost.id: respost for respost in instance.resposts.all()}
    
            for respost_data in resposts_data:
                respost_id = respost_data.get('id', None)  # Har bir respost uchun id olamiz

                if respost_id and respost_id in existing_resposts:
                    # Agar respost mavjud bo'lsa, uni yangilaymiz
                    respost = existing_resposts.pop(respost_id)
                    for attr, value in respost_data.items():
                        setattr(respost, attr, value)
                    respost.save()
                else:
                    # Agar respost mavjud bo'lmasa, yangi yaratamiz
                    Reports.objects.create(reports_name=instance, **respost_data)

            # Agar biror eski respost qolsa, uni o'chiramiz
            for respost in existing_resposts.values():
                respost.delete()

        return instance