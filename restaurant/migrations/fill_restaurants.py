import logging
from django.db import migrations

from ..data_collect import get_all_datas
_logger = logging.getLogger(__name__)

def fill_restaurants(apps, schema_editor):
    Restaurant = apps.get_model('restaurant', 'Restaurant')

    for name, address, latitude, longitude in get_all_datas():
        rest = Restaurant(name=name,
                          address=address,
                          latitude=latitude,
                          longitude=longitude,
                          )
        rest.save()


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fill_restaurants),
    ]
