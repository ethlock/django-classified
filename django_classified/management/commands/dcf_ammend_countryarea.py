from django.core.management.base import BaseCommand
from .l10n.models import AdminArea, Country

class Command(BaseCommand):
    help = "Remove unknown Admin Area with pattern '(...)'"
    
    def handle(self, **options):
        delete_list = ['disputed', 'PF99']
        AdminArea.objects.filter(name__regex=r'^\(.+\)$').delete()
        AdminArea.objects.filter(name__in=delete_list).delete()
        try:
            taiwan = Country.objects.get(printable_name='Taiwan, Province of China')
            taiwan.printable_name = 'Taiwan'
            taiwan.save()
        except:
            pass
        
