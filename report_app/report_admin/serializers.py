from rest_framework import serializers

from report_app.models import ReportsName, Reports, RespostComment



class RepostCommentAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = RespostComment
        fields = ['id', 'repost', 'comment', 'owner']



class ResportAdminSerializer(serializers.ModelSerializer):

     class Meta:
          model = Reports
          fields = [
               'id', 
               'bob', 
               'type_work', 
               'position',
              'unity',
               'quantity',
               'frame',
               'floor',
               'mark',
               'axles',
               'premises',
               'completions',
               'create_at'
          ]


class ReportsNameAdminSerializer(serializers.ModelSerializer):
    respost_comment = RepostCommentAdminSerializer(many=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'respost_comment', 'status_customer', 'status', 'admin', 'create_at']


    def update(self, instance, validated_data):
        # resposts ma'lumotlarini validated_data'dan ajratish
        comment_data = validated_data.pop('respost_comment', None)

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.status_user = validated_data.get('status_user', instance.status_user)
        instance.status_customer = validated_data.get('status_customer', instance.status_contractor)
        instance.status = validated_data.get('status', instance.status)
        instance.admin = self.context.get('admin')
        instance.save()

        # Kommentlarni yangilash yoki qo'shish
        if comment_data:
            existing_comments = {comment.id: comment for comment in instance.respost_comment.all()}
            admin = self.context.get('admin')
            for comment_data_item in comment_data:
                comment_id = comment_data_item.get('id', None)

                if comment_id and comment_id in existing_comments:
                    # Agar komment mavjud bo'lsa, uni yangilaymiz
                    comment = existing_comments[comment_id]
                    for attr, value in comment_data_item.items():
                        setattr(comment, attr, value)
                    comment.owner = admin
                    comment.save()
                else:
                    # Agar komment yangi bo'lsa, uni yaratamiz
                    RespostComment.objects.create(repost=instance, owner=admin, **comment_data_item)

        return instance