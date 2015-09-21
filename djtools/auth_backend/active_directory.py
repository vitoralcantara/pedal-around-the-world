# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from djtools.utils import get_profile_model
import ldap
from djtools.models import LdapConf

def get_ldap_conf():
    try:
        return LdapConf.objects.get(active=True)
    except:
        raise Exception(u'É necessário configurar o AdConf para usar este modo de autenticação.')

class LdapBackend:
    
    def authenticate(self, username=None, password=None):
        self.conf = get_ldap_conf()
        is_valid = self.is_valid(username, password)
        if not password or not is_valid:
            return None
        ProfileModel = get_profile_model()
        try:
            args = {self.conf.profile_username: username}
            profile = ProfileModel.objects.get(**args)
        except ProfileModel.DoesNotExist:
            return None
        
        user = User.objects.get_or_create(username=username)
        return self.create_or_update_user(user, username, profile)
    
    def sync_user(self, user, profile):
        ad_user = self.get_ldap_user(user.username)
        for f in self.conf.sync_fields.all():
            setattr(user, f.profile_field, ad_user[f.ldap_field])
            setattr(profile, f.profile_field, ad_user[f.ldap_field])
            user.email = user.email or '%s@noemail.com' % user.username
        user.save()
        profile.user = user
        profile.save()
        return user
    
    def get_ldap_user(self, username):
        l = ldap.initialize(self.conf.uri)
        l.simple_bind_s(self.conf.who, self.conf.cred)
        attrlist = list(self.conf.sync_fields.values_list('ldap_field', flat=True))
        result = l.search_ext_s(
            self.conf.base, 
            ldap.SCOPE_SUBTREE, 
            'sAMAccountName=%s' % username, attrlist)[0][1]
        
        def get_values(res, keys):
            values = dict()
            for key in keys:
                values[key] = key in res and res[key][0] or None
            return values
        
        return get_values(result, attrlist)
    
    def get_user(self,user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
    
    def is_valid(self, username=None, password=None):
        binddn = "%s@%s" % (username, self.conf.domain)
        try:
            l = ldap.open(self.conf.uri.split('//')[1].split(':')[0])
            l.simple_bind_s(binddn, password)
            l.unbind_s()
            return True
        except Exception:
            return False
