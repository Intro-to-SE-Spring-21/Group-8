[![Build Status](https://travis-ci.com/Intro-to-SE-Spring-21/Group-8.svg?branch=main)](https://travis-ci.com/Intro-to-SE-Spring-21/Group-8)
# Group-8

## Useful Sections:

[Team Members](#Leader)

[Project Goals](#Project-Goal)

[Objectives](#Objectives)

[Languages Used](#Languages-and-Techniques)

[Travis CI](#Testing-Webpage)

[Installing and running the website](#Running-the-website-for-the-first-time)

## Leader
**Lucian Murdock**

> (lmurdock12)
  
I am currently a senior Computer Science major at MSU. I am originially from Memphis, Tennessee.

## Members
**Brandon Ball**
> (bhball22)

I'm Brandon Ball. I am currently a Junior in Software Engineering.
  
**Kyle Dobbs**

> (kd766)

I am a Computer Science major from Atlanta, GA. 
  
**Natalie Albritton**

>(natalie2by4)

I am a Software Engineering major and from Huntsville, AL.


## Project Goal

The goal of this project is to develop a twitter like web application.
This application is initially designed to have three core features:

    * Post a tweet
    * Like a tweet
    * Follow another user

Here are the additional features we also developed on this website:

    * Creating a user account on the website
    * Login/Logout functionality 
    * Retweet functionality
    * Delete a tweet functionality
    * A global tweet feed on the hompage and a personalized custom tweet feed on the homepage
    * A custom User profile page that can display the user's tweets, likes, retweets, who is following them, and who they are following
    * The ability to upload a custom profile picture to your account
    * The ability to add an image to a given tweet
    * A discover like feature that shows you new accounts to follow
    * Added a search bar to be able to search for different users on the website
    * Added the ability to create and save a bio to be displayed on your profile page

By the end of this project we will developed a functional web app using modern agile principles.
We hope to learn more about software development practices in a team based agile environment. 

## Objectives 

The objective of this project is to learn the development methodoligiies of the agile system.

Main Objectives:

    * Utilize the proper project management techniques.
    * Learn how to develop a software project in a scrum based environment
    * Learn git and github
    * Learn how to create and use user stories throughout multiple sprints
    * Learn how to create a web application using the Django framwork. 

## Languages and Techniques

The bulk of our website will be powered by the Djano Framework (Python based).

Main Languages used:

    * Python
    * Javascript
    * HTML
    * CSS

Our backend database will also be powered through sqlite3.


## Testing Webpage
Follow this link to view TravisCI to see if the webpage is verified and which version
https://travis-ci.com/github/Intro-to-SE-Spring-21/Group-8

## Running the website for the first time

Use the main branch to test the latest implementation of the website.
The develop branch is for experimental new features for the website and is subject to breaking.

1. Install python with a version >= 3.6
2. Install Django using pip `pip3 install django`
3. Install git
4. Clone the with git using `git clone https://github.com/Intro-to-SE-Spring-21/Group-8.git`
5. Running the Django website:
  * On the main branch:
    1. Start the server using: `python manage.py runserver`
  * On the develop branch:
    1. Run the command: `python manage.py makemigrations MainApp`
    2. Then migrate using: `python manage.py migrate`
    3. Finally, populate the database using: `python manage.py populateDatabase`
    4. Start the server: `python manage.py runserver`


        <!--{% if request.COOKIES.feedType == "personal"}
        {% if isLiked.type == 'Retweet' %}
          <p>{{isLiked.username}} retweeted this</p>
        {% elif isLiked.type == 'Like' %}
          <p>{{isLiked.username}} liked this</p>
        {% endif %}
        {% endif %}-->