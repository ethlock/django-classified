from django.core.management.base import BaseCommand
from .l10n.models import AdminArea
import re


class Command(BaseCommand):
    help = "Empty any AdminSubarea placeholder identified by AdminSubarea type of 'Another'."
    
    def handle(self, **options):
        for admin_area in AdminArea.objects.all():
            if admin_area.adminsubarea_set.count() == 1:
                admin_subarea = admin_area.adminsubarea_set.get()
                if admin_subarea.admin_subarea_type == 'a' and re.match(r".*\(\*\)$", admin_subarea.name):
                    self.stdout.write("Removing AdminSubarea placeholder for " + admin_area.name)
                    admin_subarea.delete()
                
