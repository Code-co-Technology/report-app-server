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


class ReportsNameAdminSerializer(serializers.ModelSerializer):
    resposts = ResportAdminSerializer(many=True, required=False)
    respost_comment = RepostCommentAdminSerializer(many=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'respost_comment', 'status_customer', 'status', 'resposts', 'admin', 'create_at']


    def update(self, instance, validated_data):
        # resposts ma'lumotlarini validated_data'dan ajratish
        resposts_data = validated_data.pop('resposts', None)
        comment_data = validated_data.pop('respost_comment', None)

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.status_user = validated_data.get('status_user', instance.status_user)
        instance.status_customer = validated_data.get('status_customer', instance.status_contractor)
        instance.status = validated_data.get('status', instance.status)
        instance.admin = self.context.get('admin')
        instance.save()

        # Resposts'larni yangilash yoki qo'shish
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