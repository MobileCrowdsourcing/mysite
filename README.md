# SourceStory

A Crowdsourcing based collaborative story making application.
To start a local development server, clone the repo, and at the root directory, type :

 `python3 manage.py runserver 0.0.0.0:8000`

Although Django uses port 8000 by default, you can specify your Port of choice by :
  
  `0.0.0.0:(Your Port No.)`


The server application has been written on [Django](https://www.djangoproject.com/).

The project is deployed on an experimental basis on the URL : 
   http://crowdproject.pythonanywhere.com
   

## Idea

The idea behind this platform is to use a crowd (check definition : [Crowdsourcing](https://en.wikipedia.org/wiki/Crowdsourcing)) to perform creative tasks.
The "task" we make them perform here is to create their own stories out of images.
Image chains linked by users can be seen, and grown, by other users, thus leading to multiple stories from an image.
Our site starts off with some images of its own. It further enables people to add their own images according to their choice.

### Images
These form the basis of any story chain. We first started off with a text-only approach to build a story, but as stories grow larger, people might find it combursome to read the whole of other people's story.
Hence, we start with images, and allow people to link images into chains as they wish.
Such chains which have been made by multiple users get votes accordingly. 

### Script
After making image chains, we make users write their story for these chains. These stories depict what the user was thinking when they were linking the images together.
The stories are what form the target of the platform (as of now).

People can see each others' stories, they can vote for the stories they like, and they can also use ideas by others to write their own stories.

We run a "leaderboard" on the Home page displaying the highest number of votes any story by a user has earned.
