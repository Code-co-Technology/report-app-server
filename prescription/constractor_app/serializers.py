from rest_framework import serializers

from prescription.models import Prescriptions, PrescriptionsComment


class ContractorsPrescriptionSerializers(serializers.ModelSerializer):
    prescription_comment = serializers.ListField(
        child = serializers.CharField(max_length = 1000000),
        write_only=True, required=False
    )

    class Meta:
        model = Prescriptions
        fields = ['id', 'prescription_comment']
    
    def update(self, instance, validated_data):
        prescription_comment = validated_data.pop('prescription_comment', None)
        # Update instance fields
        instance.save()

        if prescription_comment:
            existing_comments = {comment.id: comment for comment in instance.respost_comment.all()}
            owner = self.context.get('owner')

            for comment_data_item in prescription_comment:
                comment_id = comment_data_item.get('id', None)

                if comment_id and comment_id in existing_comments:
                    # Agar komment mavjud bo'lsa, uni yangilaymiz
                    comment = existing_comments[comment_id]
                    for attr, value in comment_data_item.items():
                        setattr(comment, attr, value)
                    comment.owner = owner
                    comment.save()
                else:
                    # Agar komment yangi bo'lsa, uni yaratamiz
                    PrescriptionsComment.objects.create(prescription=instance, owner=owner, **comment_data_item)

        return instance
