from django.utils import timezone
from prescription.models import Prescriptions


def update_prescription_status():
    # Hozirgi sanani olish
    current_date = timezone.now().date()

    # Deadline o'tgan va status 'Просрочено' bo'lmagan retseptlarni olish
    expired_prescriptions = Prescriptions.objects.filter(deadline__lt=current_date, status__in=[1, 3, 5])

    # Har bir retseptni yangilash
    for prescription in expired_prescriptions:
        prescription.status = 4  # 'Просрочено'
        prescription.save()
