from django.core.management.base import NoArgsCommand
from .l10n.models import AdminArea, AdminSubarea

class Command(NoArgsCommand):
    help = "Fill in a single AdminSubarea placeholder for each AdminArea that does not have one yet."
    
    def handle_noargs(self, **options):
        for admin_area in AdminArea.objects.all():
            if not admin_area.adminsubarea_set.exists():
                print "Adding AdminSubarea placeholder for AdminArea " + admin_area.name
                AdminSubarea(admin_area=admin_area, name=admin_area.name + ' (*)', admin_subarea_type='a').save()
                 
        
