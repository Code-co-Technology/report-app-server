import json
from rest_framework import serializers
from django.shortcuts import get_object_or_404

from report_app.models import ReportsName, Reports, RespostComment, Bob, TypeWork, ReportFile



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
               'create_at'
          ]


class ReportsNameConstructorSerializer(serializers.ModelSerializer):
    resposts = ResportconstructorSerializer(many=True, required=False)
    respost_comment = RepostCommentContractorsSerializer(many=True, required=False)
    report_file = serializers.ListField(child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False),
        write_only=True, required=False)

    class Meta:
        model = ReportsName
        fields = ['id', 'name', 'respost_comment', 'status_user', 'status_contractor', 'report_file', 'status_customer', 'resposts', 'constructor', 'create_at']

    def create(self, validated_data):
        constructor = self.context.get('constructor')

        # resposts ma'lumotlarini validated_data dan ajratib oling
        respost_image = validated_data.pop('report_file', [])
        resposts_data = self.initial_data.get('resposts', '[]')
        try:
            resposts_data = json.loads(resposts_data)
        except json.JSONDecodeError:
            resposts_data = []
        reports_name = ReportsName.objects.create(**validated_data)

        
        # Foydalanuvchini context orqali bog'lab qo'shish
        reports_name.constructor = self.context.get('constructor')
        reports_name.status_contractor = 1
        reports_name.status_customer = 2
        reports_name.save()

        for index, respost_data in enumerate(resposts_data):
            bob_id = respost_data.get('bob')
            type_work_id = respost_data.get('type_work')
            position = respost_data.get('position')
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
        constructor = self.context.get('constructor')

        # resposts ma'lumotlarini validated_data'dan ajratish
        resposts_data = self.initial_data.get('resposts', '[]')
        try:
            resposts_data = json.loads(resposts_data)
        except json.JSONDecodeError:
            resposts_data = []
        comment_data = validated_data.pop('respost_comment', None)

        # ReportsName ma'lumotlarini yangilash
        instance.name = validated_data.get('name', instance.name)
        instance.status_user = validated_data.get('status_user', instance.status_user)
        instance.status_contractor = validated_data.get('status_contractor', instance.status_contractor)
        instance.status_customer = validated_data.get('status_customer', instance.status_customer)
        instance.constructor = self.context.get('constructor')
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
            constructor = self.context.get('constructor')
            for comment_data_item in comment_data:
                comment_id = comment_data_item.get('id', None)

                if comment_id and comment_id in existing_comments:
                    # Agar komment mavjud bo'lsa, uni yangilaymiz
                    comment = existing_comments[comment_id]
                    for attr, value in comment_data_item.items():
                        setattr(comment, attr, value)
                    comment.owner = constructor
                    comment.save()
                else:
                    # Agar komment yangi bo'lsa, uni yaratamiz
                    RespostComment.objects.create(repost=instance, owner=constructor, **comment_data_item)

        return instance