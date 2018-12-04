

# CCMS: A Chess Club Management System written in Django

## YouTube Video
- https://youtu.be/1NetT8cF4eI

## Software Stack

I approached this problem with respect to three main areas:
* Language (Python, PHP, JS, etc.)
* Framework, if any
* Database (SQLite3, MySQL, Postgres, etc.)

### 1. Language
As I am building this app for my chess coach back home (and he is decently technically inclined), I collaborated with him to see what he might want the app to be written in for maintenance convenience later on.

From my discussions with him, he told me to either use Python and PHP. I have worked with PHP before, but I ultimately chose Python for a couple of reasons:
* It was covered in our course pretty comprehensively. I felt I had a good grasp of how web development in Python was accomplished. Furthermore, I had basically built one in Flask, so I felt rather comfortable with the language.
* Python is a language that is extremely popular, especially for research in the medical field (bioinformatics, scraping). Since I want to pursue medicine, Python was a clear choice for me.
* The open source community for Python is very well established, and there are many modules that people have written already. For example, I used [this](https://github.com/sublee/elo) module which helps me process ratings according to the ELO format.

### 2. Django
Once I chose my language, I next needed to choose a web framework.

I had two main priorities when selecting a web framework:
* Not too bulky
* Included what I needed

My choices ultimately came down to Flask and Django. While Flask seemed like the easy choice since we used it in class, I ended up going with Django for a few reasons:
* Django comes with more out of the box. This includes security, emailing support, a user model with auth, and most importantly, and admin panel.
  * The admin panel allows a user with `superuser` status to go into the `/admin` site and perform many detailed actions with the different models created. No setup needed. Furthermore, it can be customized (as I did in the `cc_management/admin.py` file I will describe later) to display certain filters. The admin panel seemed quite useful for this use case because in case a staff member messes up certain records (players, games, etc.), a superuser can go in and `Create, Read, Update, or Delete` something and ensure everything is in working order. It can also be used to create new user accounts with different roles. Currently, the three roles are `non-staff`, `staff`, and `superuser`.
 * Django has extensive documentation available and a large community. While it is true that Django kind of "forces" you into their paradigm whereas Flask lets you pick more what you want to do, I believed that the advantages mentioned above outweighed the "restrictions."
 
 ### 3. Database
 I then chose a database for the app.

After talking to many friends, they all recommended I use Postgres over SQL. I remember watching some videos in the summer on my own free time to understand why, but after ensuring Postgres could store the most advanced data that I wanted to (a `JSON` object), I decided to just go with it.

[Here](https://www.linkedin.com/pulse/postgresql-vs-ms-sql-server-girish-chander) is a sample article documenting why Postgres is much better than SQL.

## Database Models
I will discuss how data is structured in my application. Please refer to `cc_management/models.py` to follow along. I decided to include all the models in one file. While I could have separated them into separate files and imported them, I felt that for the purposes of developing a testable app, that was more work than necessary. Perhaps later on when I decide to scale up and relations get more complicated I will do that.

Essentially, there are five main parts:
* Clubs (`class Clubs`): This system allows for management of multiple clubs. This is because my chess coach manages different clubs at different schools. However, for people managing just one club, this structure works just fine.
* Classifications for Clubs (`class Club_Classifications`): This is essentially the groups within a club. These could be arranged by skill level, rating, age, etc. at the discretion of the club manager. Classifications will apply for all clubs. I decided to not relate classifications to each club for now, as my coach uses the same classifications everywhere. This can be changed later on.
*  Player (`class Player`): Each club has many players. Thus, players are related to clubs using a `foreign key` which I call `club_id`. Thus, to create a player, you must have a club for it to refer to.
* Game (`class Game`): Each club has many games. Thus, games are related to clubs using a `foreign key` which I call `club`. Furthermore, each player can have many games. Thus, games are also related to players using a `foreign key`. Note that there are two of these since there is both a `white` and `black` player (`white_player` and `black_player` are the IDs).
* Batch (`class Batch`): When a staff member processes all the unprocessed games for a club, then a batch is created that contains a `JSON` object of information. More info about that can be found in the `README`. [Here](https://drive.google.com/open?id=1aKBJN15S8LLTZVdDvTDIrwAVXQq_ZmWe) is the screenshot with a sample batch for your convenience.

## Other Considerations
You might wonder why no users except those with `staff` or `superuser` status can edit a player's profile. Specifically, you may wonder why players themselves cannot edit their own profile.

After talking with the chess coach about this, we decided to not allow players (`non-staff`) to have any edit access. This is because for this use case, most chess club players will be young. Thus, we decided that it was better for the staff to fill in this information even though it is more work on the part of the club manager.

I also discuss this below in the section below titled `The Future` where I may eventually add user roles for players or their parents which is associated with a player. That account will then only be able to edit their own information.

## Coding Problems and Solutions
I will next go through the problems I faced and document how I solved them.

### Improving the Admin Site
When I had the initial basis of the app up (`CRUD` for players, clubs, classifications), I wanted to see what the admin site would look like. Unfortunately, the table displaying the information did not look too great. For example, for players, I could only click on a player by the name, with no ability to filter through any of the other fields, such as `club`. Thus, I looked into how to customize the admin site to display information in a certain way and to allow for filtering. I did this for the `Club`, `Player`, `Game`, and `Batch` models.

Here is a sample of what the before and after for the `Player` model looks like:
* [Before](https://drive.google.com/file/d/1PRNLCC8o1myG31VkVFfxEl2y59K9vI4O/view?usp=sharing)
* [After](https://drive.google.com/file/d/1s5mg2rKE76PlejqoQyRm9NO7QH9MrC2M/view?usp=sharing)

### Adding Filterable Tables for All Users
Initially, I tried to rely on the admin site too much. I thought that most of my app could just be built off of the admin panel that Django comes with rather than trying to build the `CRUD` operations myself.

Once I moved past that initial barrier, I realized that I needed a better way to display information. What I was doing before was just querying the database for all objects given a certain condition and custom writing HTML Bootstrap tables and taking advantage of Django's templating engine to fill in the data.

While this worked, it was not ideal for two main reasons:
* I would have to hand-code the tables for each model I wanted to display (I ended up doing this initially. :/)
* The user would not be able to interact with the data. They could not filter it, which becomes important when a club expands and may have many players or games. Then it may be useful to sort by most activate players (sort by `number of games played`), etc. It may also be useful to find all games that a certain player has played.

Thus, I searched for a solution to better display tables to all types of users.

I found the solution in using the `django_tables2` library (documentation [here](https://django-tables2.readthedocs.io/en/latest/)) to display the tables and `django_filters` (documentation [here](https://django-filter.readthedocs.io/en/master/)) to include filters with each table. The implementation of this can be found in the `cc_management/tables.py` file.

However, I faced a subproblem of...

#### Subproblem to Filterable Tables - Dynamic Filter Options
One problem I faced was that in the `Games` table for each club, I wanted to allow users to find games where the `white player` was a certain player. However, the table displayed all players in the filter list, even players not in the specific club. For example, when viewing games for `Club A`, players from `Club B` could also be selected. While this wouldn't actually affect anything since the club name must match, it was bad UI.

To fix this, I had to find a way to update the `queryset` that the filter could use. Unfortunately, there was not clear documentation for this, so I had to find the `django filters` library Google Group and ask around. This took quite a bit of time (even on Thanksgiving Day). However, I was able to figure it out!

The relevant code is passing an additional parameter when creating the `GameFilter` in the `club_games` function in `cc_management/views.py`and using that additional parameter in `GameFilter` when initialized (see `cc_management/tables.py`.

### Flashing Messages to User
Initially, when creating, updating, editing, and deleting records, I would just redirect the user back to the page I felt like they should go to with no feedback in terms of whether the desired action was successfully completed or not.

This seemed like bad UI, so I tried to search for a way to display messages after certain actions were completed.

I was able to find a builtin module in Django called messages (linked [here](https://docs.djangoproject.com/en/2.1/ref/contrib/messages/)) to flash messages.

A sample use case would be after a game is created. You can look at this in the `game_create` function in `cc_management/views.py`
* `messages.success(request, f'Game added!')`

### Displaying a different choice to the user than what is stored in the database
What does this mean? I think it's best to talk about this through example.

Let's look at the `Player` model (look in `cc_management/models.py`.

Notice that there is a `grade` field. Now good UI is where the user can select from `First, Second, Third, Fourth, etc.` rather than `1, 2, 3, 4`. However, it's not a good idea to store `First` in the database as that will be a `varchar` whereas storing `1, 2, 3, 4` are integers. Furthermore, you may want to update the options later to associate different integers with new values.

I thought I would have to just write frontend code to render the `grade` dropdown to display it, potentially using something like a dictionary. However, after reading lots of documentation, I realized that Django allows you to do this by specifying a `choices` parameter. I did this with the `grade` field for the player as well as the `result` field for the game (whether white won, black won, or draw).

The documentation I used was [here](https://docs.djangoproject.com/en/2.1/ref/models/fields/#choices).

### Having Timestamps for Games and other Models
Having timestamps is extremely useful for certain models. For example, it is tedious to enter a `played_on` date for a game if you enter the game. It is more convenient to have this automatically be inserted into the database.

Conveniently, Django has not just a `DateField` but also parameters such as `auto_now_add` which auto adds a timestamp **only** when the record is created, and `auto_now` which auto updates the timestamp anytime the record is updated.

The documentation I referred to is [here](https://docs.djangoproject.com/en/2.1/ref/models/fields/#datetimefield).

### Automatically Updating a Player's USCF Rating when a valid USCF ID is Provided
Initially, I created the Player model so that administrators would have to manually enter not only a player's UCSF ID but also manually look up their UCSF Rating and update that.

This is highly inconvenient and is not very time efficient. My chess coach found an old version of the UCSF Player lookup that I could query  (Use http://www.uschess.org/msa/thin.php? and add the relevant USCF ID).

So I tested this manually with different valid IDs, inspected the `HTML`, and found what unique HTML element contained the value I wanted (`input[name=rating1]`).

Once I had this information, I was ready to implement it. I needed to figure out two things:
1. How to make a request using python in a Django app **and** parse the request response ideally using one library.
2. How to initiate this request only after a player updates their profile.

Please refer to `cc_managemeng/signals.py` for the code for this section.

For the first, I knew of the Python `requests` library and `beautifulsoup4` library, but I didn't want to have to write a lot of code to connect them. I searched for an all-in-one library and found `requests_html`, which allows me to make a request and immediately parse it instead of writing any `bs4` code. Link [here](https://html.python-requests.org/).

For the second one, I read the Django documentation to search for any hooks or signals that may be sent enough. Sure enough, I found that Django has signals that you can respond to. Furthermore, you can respond to only certain signals. In this case, I wanted to respond to the `post-save` signal sent by a `Player` object.  Link to Django documentation for signals [here](https://docs.djangoproject.com/en/2.1/topics/signals/).

This can be implemented using the `@receiver` decorator. The rest is pretty straightforward, although I did need to implement a `try - finally` branch to prevent the profile from infinitely recursing and running each time the profile is saved.

## Other Problems

### Deploying to a DigitalOcean Droplet running an Apache Server
I thought that deploying a web app on DigitalOcean would be quite simple. After all, I just need to setup the server and move the files in the right place right? **Nope, not at all.**

I watched videos, read `DigitalOcean` documentation, wrote my own documentation for myself, and finally got it set up and running fine on `HTTP`. I learned the following:
* How to push to a remote location (in this case my local repo directly to a location on the DigitalOcean droplet)
* the `SCP` protocol and how to transfer files (before I learned how to push to a remote)

I then wanted to have the same database records for testing, so I tried to dump the `Postgres` database on my local instance and import it into the `Postgres` server running on the droplet, and it worked, but I couldn't read or write from it because the `Postgres` versions differed.

I then tried to set up `HTTPS` by generating an SSL certificate manually, but when I did that, all I got to show up was the default `Apache` page rather than my app. I could not figure this out at all for a few days.

My solution was then... to use Heroku!

### Deploying to Heroku (Let's Hope it Works... It Did :) )
I then asked some friends (including the chess coach) on what advice they might have, and they said that they recommended I try to use Heroku.

Some issues ran up there. The main ones are listed below.

I found these two resources **extremely** helpful:
* [Source 1](https://www.youtube.com/watch?v=TgmeAN32Uvw&index=7&list=PLEsfXFp6DpzTgDieSvwKL3CakR8XyKkBk)
* [Source 2](https://github.com/codingforentrepreneurs/Guides/blob/master/all/Heroku_Django_Deployment_Guide.md)

#### Different Config Variables

So locally, I was using a `.env` file and using `django-dotenv` to read in the environment variables for the database and e-mail server information, as well as the secret key for the app. However, when you push to Heroku, you don't want to push your `.env` file and there may be a race condition where you try to access a variable before Heroku reads it in.

I realized Heroku has their own config variables (linked [here](https://devcenter.heroku.com/articles/config-vars)), so I had to figure out how to access those variables.

#### Remote Postgres Server

I had no idea what the credentials for my Postgres server would be if I wasn't running Postgres anymore. However, Heroku has an add-on for Postgres that can be used. Furthermore, it's just a few lines to include the database in a python app like mine. (documentation [here](https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python))

#### Generating Static Files

Since I am no longer running the app locally, I had to generate my static files for the admin site mainly to have it all nice and bootstrapped rather than just barebones HTML.

## The Future - Scaling Up

### One more User Role
I anticipate that once this is used, it will be helpful for a parent of a player to create an account and have their account be associated with their player's information. While this won't be that useful for view purposes since anyone can view players, it can be useful for a player and/or their parent to update information. For example, when they create a UCSF ID, they can add that to their profile instead of having the staff have to enter them manually.

### Un-Processing Things
According to the chess coach, this would be quite difficult to do technically and given my time constraints, I decided that I would implement this feature later. Essentially, a helpful feature would be to unprocess already processed games, revert ratings, add more games, and then process those together. This is complex because it requires stepping back in time via batches and is not that crucial when piloting this app.

### Displaying Charts of Ratings
It is quite useful to be able to visualize a parent's rating progress over time, similar to how [CoinMarketCap](https://coinmarketcap.com/) displays cryptocurrency prices (crash, :/).

I also did not implement this yet as it also requires stepping back over time and it seemed like implementing this alongside the un-processing things would be smart.
