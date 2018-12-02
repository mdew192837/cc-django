# CCMS: A Chess Club Management System written in Django

## YouTube Video

## Summary of Project

CCMS is a website that allows for the maintenance and management of multiple chess clubs, each with many players and games. It has two types of users: staff and non-staff. Non-staff have only view access, while staff are able to add, edit, and delete things (classifications, clubs, players, games). Additionally, there exist superusers in cases where the staff may have messed something up.

### How a Staff Member can Manage a Club
1. Create classifications, which are essentially categories of players. These can be customized to what the staff would like. For example, one could create classifications titled "Pawns," "Knights," "Bishops", and "Rooks," which could represent different levels of players.
2. Create a club. This club will contain players and games.
3. Add players to the club.
4. Add games to the club. Note that at least two players must be added to the club before any games can be added.
5. Process games for a club. Games will automatically adjust player ratings.
6. Update player information. This includes updating USCF (US Chess Federation) Information, which is the official chess organization of the United States.

If given superuser access (for the founder of a chess club, for example), staff can go into the admin panel Django provides to perform some additional actions. These include:
* Filtering by player fields
* Creating more user accounts, editing passwords, etc.
* **ADD MORE INFORMATION HERE**

### Interesting Features
* When a staff member updates the USCF ID of a player, the app will automatically update the player's UCSF Rating
* Password reset. Using an SMTP server connected to the Django app, users can get a unique password reset link to the e-mail associated with their account.
* Filtered Tables. All users can view players, games, and clubs in tables that have dynamic filters for selected fields. For example, one can filter the games table by white player, black player, or game result (white won, black won, draw). Furthermore, filters within each club are unique to that club. For example, if `club A` has 5 players and `club B` has 3 players, when a user visits `club A`'s table, the filter by player will only have the 5 players for club A. Similarly, whn a user visits `club B`'s table, the filter will only have the 3 players for club B.
* **THINK OF MORE STUFF**

## Running the Project

### Testing on Heroku
If you do not want to go through setting up your own local postgres server, connecting your own SMTP mailserver and account credentials, or adding a .env file, it is strongly recommended to test the app with Heroku.

You can do so by navigating to https://ccapp-django.herokuapp.com/.

To test a non-staff account for view purposes, please just create an account.

To test a staff account, please log in with the following credentials:
* INSERT CREDENTIALS HERE

### Running Locally

#### Part I - Getting the Code and Setting up the Environment
1. First, create a virtual environment by doing the following:
	a. https://virtualenv.pypa.io/en/latest/userguide/
	b. Ensure that you are using a `virtualenv` with `Python 3.6 or greater`, as the app uses format strings which are only supported then.
2. Navigate to the project directory root (`/`).
3. Install all the requirements by running `pip install -r requirements.txt`

#### Part 2 - Setting up Postgres
You will need to setup a Postgres server running locally, create a database and user that has the permissions to edit the database (read and write to it).

Keep track of the following information (updating it with your information) and add it to a .env file in the root directory. Please ensure that the keys are **exactly the same**.
* `DATABASE_NAME=mydatabasename`
* `DATABASE_USER=mydatabase_username`
* `DATABASE_PASSWORD=mydatabase_user_password`
* `DATABASE_HOST=where_my_database_is_hosted` (usually `localhost`)

#### Part 3 - Setting up the Mail Server
To have password resets, you will need to set up the relevant mail server. The app uses the `SMTP` protocol so ensure that your e-mail server uses that.

Please keep track of the following information and add it to the `.env` file in the root directory below the database information. Please ensure that the keys are **exactly the same**
* `EMAIL_USER=myemail@mydomain.com`
* `EMAIL_PASS=myemailpassword`
* `EMAIL_HOST=smtp.myemailhostingservice.com`

#### Part 4 - Migrating the database
Now you will need to run the migrations to set up the database schema.

To do this, run the command: `python manage_old.py migrate`

Note that there will be two files `manage.py` and `manage_old.py`. `manage.py` is for the heroku install, so do not run `python manage.py migrate` but `python manage_old.py migrate`

#### Run the App!
To run the app, simply run: `python manage.py migrate`

To view the app, simply navigate to http://127.0.0.1:8000/.

## Running the App As Non-Staff

### The Homepage

By default, navigating to the home page `/` will redirect you to `/clubs` to view all chess clubs. Everything a user would want to do will be here.

Here, you will find a table of all the clubs, where you can perform the actions of:
* Viewing the players for a club
* Viewing the games associated with that club

The navbar includes a `logout` link and a `Home` URL which will take you back to the clubs table.

### Logging In / Out
As discussed above, you will be prompted to login when you try to access the root page. Once logged in, a `Logout` link will appear on the top right corner of the navbar.

### Signing Up
If you are not logged into the app, you will be redirected to the login page.

There, you will find a button to `Sign Up Now` if you haven't signed up.

Once you sign up, you will be redirected to the `login` page again, where you can log in. Once you log in, you will be redirected to the `/clubs` page.

### Forgot Password
If you forget your password, you can click the `Forgot Password` button that is in the `login` page.

Once you enter the e-mail associated with the account, then you will receive an e-mail with a unique link to reset your password. Once you reset your password, then you will be shown a `Sign In Here` button to login again.

## Running the App As Staff
Most functionality will be the same. You can still view games, players, and clubs. The main difference is that different buttons will appear that allow you to add games, players, or edit club information.

### Additional Features for Staff
Note that all desired actions can always be accessed via buttons in the table on the homepage.
* Add a game to a specific club by the clicking the `Add Game` button. Note that you can only do this if you have two or more players in that club.
* Add a player to a specific club by clicking the `Add Player` button. Required fields will be marked with an asterisk and you will receive a bootstrap hint via JS if you do not fill out a required field. If you disable javascript, there is also backend authentication. This applies to similar CRUD features.
  * Cool feature. If you add a player's USCF ID (mine is 13778174), then the app will automatically fetch the player's USCF rating once the profile is saved.
* Edit a game. Note that you cannot edit the players for a game, only the result of the game. Furthermore, this will not reprocess ratings as of now, as I was unable to figure out stepping back in time at this point.
* Edit a club. This will just be the club name.
* Edit a player's information. This can be accessed by clicking the `View Players` button in the `clubs` table and clicking the `Edit` button associated with the player whose information you would like to edit.
* Modify classifications by clicking the `Classifications` link in the navbar. Editing it will allow you to edit the name of the classification. Deleting it will delete the classification, including all players in the classification, so this is highly discouraged. If this is necessary, one should reassign each player in the classification to another classification. There is no automatic way to do this yet.

### Processing Games
This is the key feature of this application. When games are created for a club, they are marked as unprocessed. If there is at least one unprocessed game in a club's games table, then a `Process Games` button will show at the bottom of the table for **staff only**.

Clicking this will do the following:
* Go through all unprocessed games for the club. It will process all games according to the [ELO rating system](https://en.wikipedia.org/wiki/Elo_rating_system). This will:
  * Update ratings for all players (after it goes through all games. This is because players may have played multiple games and we want to process games based on the previous rating of the player. This is done by processing each game using the current player rating, calculating and storing the rating differential for that game, and then summing those at the end to update the player rating)
  * Update the `games played` for each player
  * Mark each game as processed
* It will also create a batch, which contains the `club name`, `processed_on date`, and a `JSON` object that has:
  * An array of the IDs of the games processed in that batch
  * A players object which contains players by ID and more information (rating before, rating after, net rating differential) 

### Admin Site
If the staff user is made a superuser (see here for information on how to do that), then the user can access the admin site via the `Admin` link (just `sampledomain.com/admin`) that will appear in the navbar in the upper right hand corner.

Here, the superuser can perform the actions mentioned above in addition to having access to some more sophisticated filters in each section.

Also, the superuser can click the `Users` link to add new users. They can also promote a user to have staff privileges or to have superuser privileges.