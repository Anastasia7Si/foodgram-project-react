from csv import reader

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Загрузка данных из csv-файлов в базу данных'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных началась')
        )

        with open('recipes/data/ingredients.csv',
                  encoding='utf-8', mode='r') as ingredients:
            for row in reader(ingredients):
                if len(row) == 2:
                    Ingredient.objects.get_or_create(
                        name=row[0], measurement_unit=row[1],
                    )

        self.stdout.write(
            self.style.SUCCESS('Загрузка данных завершена')
        )
