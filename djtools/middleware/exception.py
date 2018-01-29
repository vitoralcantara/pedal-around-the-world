# -*- coding: utf-8 -*-

from django.views.debug import technical_500_response
import sys

class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())


#from django.views.debug import technical_500_response
#import sys
#from django.conf import settings
#from django.core.mail import mail_admins
#
#class AnotherExceptionMiddleware(object):
#    
#    def _get_traceback(self, exc_info=None):
#        "Helper function to return the traceback as a string"
#        import traceback
#        return '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info())))
#    
#    def process_exception(self, request, exception):
#        exc_info = sys.exc_info()
#        user_info = unicode(request.user)
#        try:
#            user_profile = request.user.get_profile()
#            user_info += u' - ' + unicode(user_profile)
#        except Exception, e:
#            print e
#        message = u"Usuário: %s\n\n%s\n\n%s" % (user_info, self._get_traceback(exc_info), repr(request))
#        mail_admins('SUAP - Erro', message, fail_silently=True)
#        
#        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
#            return technical_500_response(request, *sys.exc_info())
