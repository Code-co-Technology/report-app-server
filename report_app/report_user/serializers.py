from rest_framework import serializers

from report_app.reports.serializers import BobSerializers, TypeOfWorkSerializer
from report_app.models import ReportsName, Reports, RespostComment


class RepostCommentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = RespostComment
        fields = ['id', 'repost', 'comment', 'owner']


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
    respost_comment = RepostCommentUserSerializer(many=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'status_user', 'status_contractor', 'resposts', 'respost_comment', 'user', 'create_at']

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
        comment_data = validated_data.pop('respost_comment', None)

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.status_user = validated_data.get('status_user', instance.status_user)
        instance.status_contractor = validated_data.get('status_contractor', instance.status_contractor)
        instance.save()
        
        if resposts_data is not None:
            existing_resposts = {respost.id: respost for respost in instance.resposts.all()}

            for respost_data_item in resposts_data:
                respost_id = respost_data_item.get('id', None)

                if respost_id and respost_id in existing_resposts:
                    # Agar respost mavjud bo'lsa, uni yangilaymiz
                    respost = existing_resposts[respost_id]
                    
                    for attr, value in respost_data_item.items():
                        setattr(respost, attr, value)
                    respost.save()
                else:
                    # Agar respost yangi bo'lsa, uni yaratamiz
                    # Use filter() instead of get_or_create()
                    new_respost = Reports.objects.filter(reports_name=instance, **respost_data_item).first()
                    if not new_respost:
                        Reports.objects.create(reports_name=instance, **respost_data_item)

        # Kommentlarni yangilash yoki qo'shish
        if comment_data:
            existing_comments = {comment.id: comment for comment in instance.respost_comment.all()}
            user = self.context.get('user')

            for comment_data_item in comment_data:
                comment_id = comment_data_item.get('id', None)

                if comment_id and comment_id in existing_comments:
                    # Agar komment mavjud bo'lsa, uni yangilaymiz
                    comment = existing_comments[comment_id]
                    for attr, value in comment_data_item.items():
                        setattr(comment, attr, value)
                    comment.owner = user
                    comment.save()
                else:
                    # Agar komment yangi bo'lsa, uni yaratamiz
                    RespostComment.objects.create(repost=instance, owner=user, **comment_data_item)

        return instance