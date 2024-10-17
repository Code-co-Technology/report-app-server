from rest_framework import serializers

from report_app.models import ReportsName, Reports, RespostComment



class RepostCommentContractorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RespostComment
        fields = ['id', 'repost', 'comment', 'owner']



class ResportconstructorSerializer(serializers.ModelSerializer):

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


class ReportsNameConstructorSerializer(serializers.ModelSerializer):
    resposts = ResportconstructorSerializer(many=True, required=False)
    respost_comment = RepostCommentContractorsSerializer(many=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'respost_comment', 'status_user', 'status_contractor', 'resposts', 'constructor', 'create_at']

    def create(self, validated_data):
        # resposts ma'lumotlarini validated_data dan ajratib oling
        resposts_data = validated_data.pop('resposts')
        
        # ReportsName ni yaratish
        reports_name = ReportsName.objects.create(**validated_data)
        
        # Foydalanuvchini context orqali bog'lab qo'shish
        reports_name.constructor = self.context.get('constructor')
        reports_name.status_contractor = 1
        reports_name.status_customer = 2
        reports_name.save()

        # Har bir respost uchun alohida Reports obyektlarini yaratish
        for respost_data in resposts_data:
            Reports.objects.create(reports_name=reports_name, **respost_data)

        return reports_name

    def update(self, instance, validated_data):
        # resposts ma'lumotlarini validated_data'dan ajratish
        resposts_data = validated_data.pop('resposts', None)
        comment_data = validated_data.pop('respost_comment', None)

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.status_user = validated_data.get('status_user', instance.status_user)
        instance.status_contractor = validated_data.get('status_contractor', instance.status_contractor)
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

        if comment_data:
            # Mavjud resposts'larni id bo'yicha olamiz
            existing_resposts = {respost.id: respost for respost in instance.respost_comment.all()}
    
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
                    RespostComment.objects.create(repost=instance, **respost_data)

            # Agar biror eski respost qolsa, uni o'chiramiz
            for respost in existing_resposts.values():
                respost.delete()

        return instance