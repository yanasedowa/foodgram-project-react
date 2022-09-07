import csv

from colorama import Fore, init
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

init(autoreset=True)


class Command(BaseCommand):
    """Management-команда наполняющей базу данных тестовыми данными
    """
    help = ('Helps to fill the database with test '
            'data from "/data"')

    def fill_table_ingredients(self):
        self.stdout.write(
            '  Applying /data/ingredients.csv', ending='... '
        )
        try:
            with open('data/ingredients.csv',
                      encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                for row_num, row in enumerate(reader):
                    if row_num == 0:
                        continue
                    else:
                        Ingredient.objects.get_or_create(
                            name=row[0],
                            measurement_unit=row[1]
                        )
            return self.stdout.write(Fore.GREEN + 'OK')
        except Exception as error:
            self.stderr.write(Fore.RED + 'FALSE')
            raise Exception(error)
        finally:
            csvfile.close()

    def handle(self, *args, **options):
        self.stdout.write(
            'Operations to perform:\n'
            + '  Filling the database with test data '
            + 'from /data/\n'
            + 'Running filling database:'
        )
        try:
            self.fill_table_ingredients()
        except Exception as error:
            self.stderr.write(
                Fore.RED + f'Execution error - {error}!'
            )
