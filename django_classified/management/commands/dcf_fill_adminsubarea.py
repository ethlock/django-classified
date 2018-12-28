from django.core.management.base import BaseCommand
from .l10n.models import AdminArea, AdminSubarea

class Command(BaseCommand):
    help = "Fill in a single AdminSubarea placeholder for each AdminArea that does not have one yet."
    
    def handle(self, **options):
        for admin_area in AdminArea.objects.all():
            if not admin_area.adminsubarea_set.exists():
                self.stdout.write("Adding AdminSubarea placeholder for AdminArea " + admin_area.name)
                AdminSubarea(admin_area=admin_area, name=admin_area.name + ' (*)', admin_subarea_type='a').save()
                 
        
