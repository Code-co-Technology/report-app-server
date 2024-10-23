from rest_framework import serializers

from report_app.models import ReportsName, Reports, RespostComment


class RepostCommentCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = RespostComment
        fields = ['id', 'repost', 'comment', 'owner']


class ResportCustomerSerializer(serializers.ModelSerializer):

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
               'create_at'
          ]


class ReportsNameCustomerSerializer(serializers.ModelSerializer):
    resposts = ResportCustomerSerializer(many=True, required=False)
    respost_comment = RepostCommentCustomerSerializer(many=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'respost_comment', 'status_contractor', 'status_customer', 'status', 'resposts', 'customer', 'create_at']

    def create(self, validated_data):
        # resposts ma'lumotlarini validated_data dan ajratib oling
        resposts_data = validated_data.pop('resposts')
        
        # ReportsName ni yaratish
        reports_name = ReportsName.objects.create(**validated_data)
        
        # Foydalanuvchini context orqali bog'lab qo'shish
        reports_name.customer = self.context.get('customer')
        reports_name.status_customer = 2
        reports_name.status = 1
        reports_name.save()

        # Har bir respost uchun alohida Reports obyektlarini yaratish
        for respost_data in resposts_data:
            Reports.objects.create(reports_name=reports_name, **respost_data)

        return reports_name

    def update(self, instance, validated_data):
        customer = self.context.get('customer')
         # Tekshirish: foydalanuvchi hisobot yubora oladimi yoki yo'q
        if customer.report_processing:
            raise serializers.ValidationError({"error": "У вас нет разрешения на обработку отчета"})
        # resposts ma'lumotlarini validated_data'dan ajratish
        resposts_data = validated_data.pop('resposts', None)
        comment_data = validated_data.pop('respost_comment', None)

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.status_user = validated_data.get('status_user', instance.status_user)
        instance.status_contractor = validated_data.get('status_contractor', instance.status_contractor)
        instance.status_customer = validated_data.get('status_customer', instance.status_customer)
        instance.status = validated_data.get('status', instance.status)
        instance.customer = self.context.get('customer')
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
            customer = self.context.get('customer')
            for comment_data_item in comment_data:
                comment_id = comment_data_item.get('id', None)

                if comment_id and comment_id in existing_comments:
                    # Agar komment mavjud bo'lsa, uni yangilaymiz
                    comment = existing_comments[comment_id]
                    for attr, value in comment_data_item.items():
                        setattr(comment, attr, value)
                    comment.owner = customer
                    comment.save()
                else:
                    # Agar komment yangi bo'lsa, uni yaratamiz
                    RespostComment.objects.create(repost=instance, owner=customer, **comment_data_item)

        return instance