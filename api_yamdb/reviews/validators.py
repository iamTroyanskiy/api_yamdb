from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_title_year(value):
     now = timezone.now().year
     if value > now:
        raise ValidationError(
            ('Год выпуска %(value)s больше текущего.'),
            params={'value': value},
        )
