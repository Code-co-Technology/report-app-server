from django.utils import timezone
from prescription.models import Prescriptions


def update_prescription_status():
    # Hozirgi sanani olish
    current_date = timezone.now().date()

    # Deadline o'tgan va hali 'Просрочено' bo'lmagan retseptlarni olish
    expired_prescriptions = Prescriptions.objects.filter(deadline__lt=current_date, status__in=[1, 3, 5])

    # Bir martalik yangilash
    expired_prescriptions.update(status=4)  # Barcha tanlangan retseptlarni "Просрочено"ga o'zgartirish