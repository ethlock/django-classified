import os
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from xml.dom.minidom import parse
from django_classified.l10n.models import Country, Currency


class Command(BaseCommand):
    help = "Load currency data from ISO 4217:2008 comprising information on currency, alphabetic code, minor unit and linked to l10n.models.Country"
    
    def handle(self, **options):
        datasource = open(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'fixtures', 'dl_iso_table_a1.xml'))
        dom = parse(datasource)
        _handle_isocurrency(dom)
        
def _get_text(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def _handle_isocurrency(ccycodes):
    
    for isocurrency in ccycodes.getElementsByTagName('ISO_CURRENCY'):
        entity = _get_text(isocurrency.getElementsByTagName('ENTITY')[0].childNodes)
        if entity and entity != 'ANTARTICA':
            try:
                country = Country.objects.get(name=entity)
            except ObjectDoesNotExist:
                continue
            currency = _get_text(isocurrency.getElementsByTagName('CURRENCY')[0].childNodes)
            alphabetic_code = _get_text(isocurrency.getElementsByTagName('ALPHABETIC_CODE')[0].childNodes)
            numeric_code = _get_text(isocurrency.getElementsByTagName('NUMERIC_CODE')[0].childNodes)
            minor_unit = _get_text(isocurrency.getElementsByTagName('MINOR_UNIT')[0].childNodes)
            try:
                item= Currency.objects.get(country=country,currency=currency)
            except ObjectDoesNotExist:
                item = Currency(country=country, currency=currency)
            item.alphabetic_code = alphabetic_code
            if numeric_code:
                item.numeric_code = int(numeric_code)
            if minor_unit:
                item.minor_unit = int(minor_unit)
            item.save()
