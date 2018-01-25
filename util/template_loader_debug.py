from django.template import (
    engine as dj_eng,
    exceptions as dj_exceptions,
    Template
)

from django.template.exceptions import TemplateDoesNotExist

import traceback

def custom_get_template(self, template_name, TemplateDoesNotExist, Template, skip=None):
    """
    Call self.get_template_sources() and return a Template object for
    the first template matching template_name. If skip is provided, ignore
    template origins in skip. This is used to avoid recursion during
    template extending.
    """
    tried = []

    for origin in self.get_template_sources(template_name):
        print('\t\t{0}'.format(origin))
        if skip is not None and origin in skip:
            tried.append( (origin, 'Skipped') )
            continue

        try:
            contents = self.get_contents(origin)
        except TemplateDoesNotExist:
            tried.append((origin, 'Source does not exist'))
            continue
        else:
            print("\t\t\tTEMPLATE FOUND!")
            return Template(
                contents, origin, origin.template_name, self.engine,
            )
    print("\t\tNOUGHT FOUND, RAISING EXCEPTION!")
    raise TemplateDoesNotExist(template_name, tried=tried)

""" 
You may notice that I am passing an EXCEPTION into this function.
This was the ONLY WAY I could get this function to work properly.
An error of that magnitude is certainly indicative of terrible things afoot.
"""
def custom_find_template(self, name, TemplateDoesNotExist, cust_get_temp, Template, dirs=None, skip=None):

    tried = []
    i = 0
    for loader in self.template_loaders:
        try:
            print( '\t{0}: {1}'.format(i, name) )
            print( '\t   {0}'.format(loader) )

            template = cust_get_temp(loader, name, TemplateDoesNotExist, Template, skip=skip)
            return template, template.origin
        except TemplateDoesNotExist as e:
            print( '\t   LOADER COULD NOT FIND TEMPLATE'.format(loader) )
            if i == 1:
                print( '\t   SPECIAL BRUTEFORCE TRACEBACK'.format(loader) )
                traceback.print_exc()
            tried.extend(e.tried)
        i += 1
    raise TemplateDoesNotExist(name, tried=tried)

defaulted = dj_eng.Engine.get_default()

try:
    print('THEORETICAL ROUTES: ')
    for loader in defaulted.template_loaders:
        for item in loader.get_dirs():
            print(item)
            print('\t' + item + '/my_dashboard.html')
    print()
    print('FIND THE TEMPLATE: ')
    #defaulted.find_template(defaulted, 'my_dashboard.html')
    custom_find_template(defaulted, 'my_dashboard.html', TemplateDoesNotExist, custom_get_template, Template)
except TemplateDoesNotExist as e:
    print('ERROR RESULTS:')

    print('\tTRIED')
    for t, m in e.tried:
        print( '\t\t{0}'.format( m ) )
        print( '\t\t{0}'.format(t.name) )
        print( '\t\t{0}'.format( type(t.name) ) )
        print( '\t\t{0}'.format(t.template_name) )
        print( '\t\t{0}'.format(t.loader) )
        print( )
        """
        if t.loader:
            print( '\t\t\t{0}'.format(t.loader) )
            print( '\t\t\t{0}'.format(t.loader) )
            print( '\t\t\t{0}'.format(t.loader) )
        """
    print('\tCHAIN')
    for c in e.chain:
        print( '\t\t' + str(c) )

    print('\tTRACE')
    traceback.print_exc()