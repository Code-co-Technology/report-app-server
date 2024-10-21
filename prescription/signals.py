from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from prescription.models import Prescriptions


@receiver(post_save, sender=Prescriptions)
def check_deadline(sender, instance, **kwargs):
    # Hozirgi sanani olish
    current_date = timezone.now().date()

    # Agar deadline o'tgan bo'lsa va status hali 'Просрочено' bo'lmasa
    if instance.deadline < current_date and instance.status != 4:
        instance.status = 4  # 'Просрочено'
        # status ni saqlash uchun `update_fields`dan foydalaning
        instance.save(update_fields=['status'])
