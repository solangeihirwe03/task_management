from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Check if the database connection is working"

    def handle(self, *args, **options):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
                result = cursor.fetchone()
                if result:
                    self.stdout.write(self.style.SUCCESS('Database connection successful!'))
                else:
                    self.stdout.write(self.style.ERROR("Database connection failed: No result returned"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Database connection failed: {e}" ))