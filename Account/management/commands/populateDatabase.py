from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from Account.models import Follow
import os


class Command(BaseCommand):
    help = 'Creates and saves several of all of the models in our database (Users, Tweets, and Follows)'

    def handle(self,*args,**options):

        user_1 = User(username='lmurdock12',first_name='Lucian',last_name='Murdock',email='lcm388@msstate.edu')
        user_1.set_password('lmurdock12')
        user_2 = User(username='bhball22',first_name='Brandon',last_name='Ball',email='bhbal22@msstate.edu')
        user_2.set_password('bhball22')
        user_3 = User(username='natalie2by4',first_name='Natalie',last_name='Albritton',email='natalie2by4@msstate.edu')
        user_3.set_password('natalie2by4')
        user_4 = User(username='kd766',first_name='Kyle',last_name='Dobbs',email='kd766@msstate.edu')
        user_4.set_password('kd766')


        User.objects.create_superuser('admin','admin@msstate.edu','admin')

        user_5 = User(username='bagely',first_name='Bagley',last_name='School',email='bagely@msstate.edu')
        user_5.set_password('bagely')

        user_6 = User(username='github',first_name='Git',last_name='Hub',email='github@msstate.edu')
        user_6.set_password('github')

        user_7 = User(username='bobross',first_name='bob',last_name='ross',email='bobross@msstate.edu')
        user_7.set_password('bobross')

        user_8 = User(username='drake',first_name='drake',last_name='',email='drake@msstate.edu')
        user_8.set_password('drake')

        user_9 = User(username='oprahwinfrey',first_name='Oprah',last_name='Winfrey',email='oprahwinfrey@msstate.edu')
        user_9.set_password('oprahwinfrey')

        user_10 = User(username='billgates',first_name='bill',last_name='gates',email='billgates@msstate.edu')
        user_10.set_password('billgates')

        user_1.save()
        user_2.save()
        user_3.save()
        user_4.save()
        user_5.save()
        user_6.save()
        user_7.save()
        user_8.save()
        user_9.save()
        user_10.save()
        #admin.save()

        follow_dict = {
            'lmurdock12':[user_10,user_1,user_4,user_6],
            'bhball22':[user_2,user_7,user_8],
            'natalie2by4':[user_7,user_2,user_8,user_4,user_3],
            'kd766':[user_8,user_1,user_5,user_3,user_7,user_6],
            'admin':[user_4,user_1],
            'bagely':[user_3,user_9,user_5],
            'github':[user_3],
            'bobross':[user_2,user_3,user_5,user_9,user_10],
            'drake':[user_6,user_7],
            'oprahwinfrey':[user_5,user_2,user_7,user_4],
            'billgates':[user_10,user_7,user_3]
        }

        for key,value in follow_dict.items():

            user_following = User.objects.get(username=key)
            
            for i in range(len(value)):

                follow = Follow(user=user_following,following=value[i])
                follow.save()
        
