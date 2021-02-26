from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from Account.models import Follow
from Account.models import Tweet
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

        user_5 = User(username='bagley',first_name='Bagley',last_name='School',email='bagely@msstate.edu')
        user_5.set_password('bagley')

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
            'bagley':[user_3,user_9,user_5],
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




        post_1 = Tweet.objects.create(tweet_creator=User.objects.get(pk=11), tweet_text="Recent extreme weather events are a stark reminder that we’re already seeing the effects of climate change here at home and around the world. This type of observation system will help scientists monitor and predict future weather events.", pub_date='2021-02-26 10:30:00.000000')
        post_2 = Tweet.objects.create(tweet_creator=User.objects.get(pk=11), tweet_text="To avoid a climate disaster, we need to eliminate emissions from the ways we create electricity, grow food, make things, move around, and heat and cool our buildings. It won’t be easy, but I believe we can do it. This book is about what it will take.", pub_date='2021-02-14 09:17:00.000000')
        post_3 = Tweet.objects.create(tweet_creator=User.objects.get(pk=10), tweet_text="I want a chance to do for you what you do for me! #QueenSugar", pub_date='2021-02-16 08:00:00.000000')
        post_4 = Tweet.objects.create(tweet_creator=User.objects.get(pk=10), tweet_text="The path to a stronger, healthier life, begins with the love we bring ourselves. Which is why this Valentine’s Day weekend, @ww_us and I are hosting Oprah’s Your Life In Focus: Be The Love You Need, a live virtual experience that will help you activate the life you most desire.", pub_date='2021-02-4 08:16:00.000000')
        post_5 = Tweet.objects.create(tweet_creator=User.objects.get(pk=7), tweet_text="Some of our favorite moments from the #GitHubUniverse keynote. See the full version and all sessions, now on demand, githubuniverse.com", pub_date='2020-12-14 11:02:00.000000')
        post_6 = Tweet.objects.create(tweet_creator=User.objects.get(pk=9), tweet_text="Congrats on 20 years!", pub_date="2021-02-22 16:15:00.000000")
        post_7 = Tweet.objects.create(tweet_creator=User.objects.get(pk=9), tweet_text="Like a good neighbor @JakeSateFarm #ad", pub_date='2021-02-07 6:46:00.000001')
        post_8 = Tweet.objects.create(tweet_creator=User.objects.get(pk=8), tweet_text='"This is a nice place. My mother\'d like a place like this. She likes these quiet little places where the water plays."\nFrom The Joy of Painting Series 12 Episode 8', pub_date="2021-02-26 16:01:00.000000")
        post_9 = Tweet.objects.create(tweet_creator=User.objects.get(pk=8), tweet_text="Registration ends March 1 for the Bob Ross Run for the Trees Virtual 5K! International participants are welcome. Every step counts! All proceeds support Happy Little Tree planting and preservation efforts in Michigan state parks.Register now at https://bit.ly/2KVb2HU", pub_date="2021-02-26 21:45:00.000000")
        post_10 = Tweet.objects.create(tweet_creator=User.objects.get(pk=6), tweet_text="That's it for our Virtual Student Organization Fair. If you missed any videos, you can check out the #BCoEvirtualorgfair hashtag. Or see the complete playlist over on our YouTube channel. Be sure to hit that subscribe button while you're there.", pub_date="2021-09-25 15:30:00.000000")
        post_11 = Tweet.objects.create(tweet_creator=User.objects.get(pk=6), tweet_text="Engineering alumni are well-represented on the @MSU_Foundation board of directors. #WeRingTrue #HailState", pub_date="2021-02-26 14:47:00.00000")
        post_12 = Tweet.objects.create(tweet_creator=User.objects.get(pk=3), tweet_text="Congratulations, we were told diddly squat about this project! #Confusion", pub_date="2021-01-25 15:33:25.16748")
        post_13 = Tweet.objects.create(tweet_creator=User.objects.get(pk=4), tweet_text="It is definitely not February but it's not not February :)", pub_date="2021-02-28 12:00:00.000000")
        post_14 = Tweet.objects.create(tweet_creator=User.objects.get(pk=5), tweet_text="And the Lord spake, saying, 'First shalt thou take out the Holy Pin. Then shalt thou count to three, no more, no less. Three shall be the number thou shalt count, and the number of the counting shall be three. Four shalt thou not count, neither count thou two, excepting that thou", pub_date="2021-02-14 11:59:59.999999")
        post_15 = Tweet.objects.create(tweet_creator=User.objects.get(pk=5), tweet_text="then proceed to three. Five is right out. Once the number three, being the third number, be reached, then lobbest thou thy Holy Hand Grenade of Antioch towards thy foe, who, being naughty in My sight, shall snuff it.'\nBook of Armaments, chapter 2: 13-21", pub_date="2021-02-14 12:00:00.000000")
        post_16 = Tweet.objects.create(tweet_creator=User.objects.get(pk=4), tweet_text="Happy Birthday", pub_date="1999-05-28 08:03:59.500000")
