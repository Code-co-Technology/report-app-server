import json
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from authen.models import CustomUser
from report_app.models import ReportsName, Reports, RespostComment, Bob, TypeWork, ReportFile


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


class ReportsNameCustomerSerializer(serializers.ModelSerializer):
    resposts = ResportCustomerSerializer(many=True, required=False)
    respost_comment = RepostCommentCustomerSerializer(many=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'respost_comment', 'status_contractor', 'status_customer', 'status', 'resposts', 'customer', 'create_at']

    def create(self, validated_data):
        # resposts ma'lumotlarini validated_data dan ajratib oling
        respost_image = validated_data.pop('report_file', [])
        resposts_data = self.initial_data.get('resposts', '[]')
        try:
            resposts_data = json.loads(resposts_data)
        except json.JSONDecodeError:
            resposts_data = []
        
        # ReportsName ni yaratish
        reports_name = ReportsName.objects.create(**validated_data)
        
        # Foydalanuvchini context orqali bog'lab qo'shish
        reports_name.customer = self.context.get('customer')
        reports_name.status_customer = 2
        reports_name.status = 1
        reports_name.save()

        # Har bir respost uchun alohida Reports obyektlarini yaratish
        for index, respost_data in enumerate(resposts_data):
            bob_id = respost_data.get('bob')
            type_work_id = respost_data.get('type_work')
            position = respost_data.get('position')
            unity = respost_data.get('unity')
            quantity = respost_data.get('quantity')
            frame = respost_data.get('frame')
            floor = respost_data.get('floor')
            mark = respost_data.get('mark')
            axles = respost_data.get('axles')
            premises = respost_data.get('premises')
            completions = respost_data.get('completions')
            
            bob = get_object_or_404(Bob, id=bob_id)
            type_work = get_object_or_404(TypeWork, id=type_work_id)
            
            if index < len(respost_image):
                report_file = respost_image[index]
                reports_instance = Reports.objects.create(
                    reports_name=reports_name,
                    bob=bob, 
                    type_work=type_work,
                    position=position,
                    unity=unity,
                    quantity=quantity,
                    frame=frame,
                    floor=floor,
                    mark=mark,
                    axles=axles,
                    premises=premises,
                    completions=completions
                )
                ReportFile.objects.create(report_file=reports_instance, file=report_file)

        return reports_name

    def update(self, instance, validated_data):
        
        # resposts ma'lumotlarini validated_data'dan ajratish
        resposts_data = self.initial_data.get('resposts', '[]')
        try:
            resposts_data = json.loads(resposts_data)
        except json.JSONDecodeError:
            resposts_data = []
        comment_data = validated_data.pop('respost_comment', None)

        customer = self.context.get('customer')
        if not isinstance(customer, CustomUser):
            raise ValueError("Customer must be a CustomUser instance")


        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.status_user = validated_data.get('status_user', instance.status_user)
        instance.status_contractor = validated_data.get('status_contractor', instance.status_contractor)
        instance.status_customer = validated_data.get('status_customer', instance.status_customer)
        instance.status = validated_data.get('status', instance.status)
        instance.customer = customer
        instance.save()

        # Resposts'larni yangilash yoki qo'shish
        existing_resposts = {respost.id: respost for respost in instance.resposts.all()}

        # Respostlarni yangilash
        for respost_data_item in resposts_data:
            respost_id = respost_data_item.get('id', None)

            # Bob va TypeWork instansiyalarini olish
            bob_id = respost_data_item.get('bob')
            type_work_id = respost_data_item.get('type_work')
            bob_instance = get_object_or_404(Bob, id=bob_id)
            type_work_instance = get_object_or_404(TypeWork, id=type_work_id)

            position = respost_data_item.get('position')
            unity = respost_data_item.get('unity')
            quantity = respost_data_item.get('quantity')
            frame = respost_data_item.get('frame')
            floor = respost_data_item.get('floor')
            mark = respost_data_item.get('mark')
            axles = respost_data_item.get('axles')
            premises = respost_data_item.get('premises')
            completions = respost_data_item.get('completions')

            if respost_id and respost_id in existing_resposts:
                # Mavjud respostni yangilash
                respost = existing_resposts[respost_id]
                respost.bob = bob_instance 
                respost.type_work = type_work_instance
                respost.position=position,
                respost.unity = unity,
                respost.quantity=quantity,
                respost.frame=frame,
                respost.floor=floor,
                respost.mark=mark,
                respost.axles=axles,
                respost.premises=premises,
                respost.completions=completions
                respost.save()
            else:
                # Yangi respost yaratish
                Reports.objects.create(
                    reports_name=instance,
                    bob=bob_instance,
                    type_work=type_work_instance,
                    position=position,
                    quantity=quantity,
                    frame=frame,
                    floor=floor,
                    mark=mark,
                    axles=axles,
                    premises=premises,
                    completions=completions
                )

        # Kommentlarni yangilash yoki qo'shish
        if comment_data:
            existing_comments = {comment.id: comment for comment in instance.respost_comment.all()}
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