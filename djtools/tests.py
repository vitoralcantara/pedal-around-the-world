# -*- coding: utf-8 -*-

from datetime import date, datetime
from decimal import Decimal
from djtools.formwidgets import BrDinheiroWidget, BrDataHoraWidget
from django.test import TestCase

def get_xml_attr(elem_as_str, attr):
    from xml.etree import ElementTree
    elem = ElementTree.fromstring(elem_as_str)
    return elem.get(attr)

class BrDataHoraWidgetTest(TestCase):
    def setUp(self):
        pass
     
    def test(self):
        w = BrDataHoraWidget()
        self.assertEquals(get_xml_attr(w.render(u'datahora', ''), 'value'), None)
        self.assertEquals(get_xml_attr(w.render(u'datahora', '31/12/2000 12:50:59'), 'value'), 
                          '31/12/2000 12:50:59')
        self.assertEquals(get_xml_attr(w.render(u'datahora', datetime(2000,12,31,12,50,59)), 'value'), 
                          '31/12/2000 12:50:59')
        

class BrDinheiroWidgetTest(TestCase):
    def setUp(self):
        pass

    def test(self):
        w = BrDinheiroWidget()
        self.assertEquals(w._format_value(None), u'')
        self.assertEquals(w._format_value(u''), u'')
        self.assertEquals(w._format_value(u'10,00'), u'10,00')
        self.assertEquals(w._format_value(u'1.000,00'), u'1.000,00')
        self.assertEquals(w._format_value(Decimal('10.00')), u'10,00')
        self.assertEquals(w._format_value(Decimal('1000.00')), u'1.000,00')
       
