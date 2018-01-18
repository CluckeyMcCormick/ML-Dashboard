from django.contrib.auth.models import User

from table import Table
from table.utils import A
from table.columns import Column

from .custom_columns import *

#_  _ ____ ____ ____ 
#|  | [__  |___ |__/ 
#|__| ___] |___ |  \ 
#                    
class UserTable(Table):

    username = CustomNoneColumn(field='username', header='Username')
    contact_name = CustomNoneColumn(field='contact', header='Contact Name', none_str='<strong>ERROR! NO CONTACT!</strong>')
    is_staff = CheckOnlyColumn(field='is_staff', header='Is Staff?')
    is_superuser = CheckOnlyColumn(field='is_superuser', header='Is Superuser?')
    email = CustomNoneColumn(field='contact.email', header='Contact Email')

    class Meta:
        model = User
        search = True

        attrs = {'class': 'table-striped table-hover'}           
