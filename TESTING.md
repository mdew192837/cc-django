To facilitate your testing and reviewing (since you may not be familiar with the workflow of running a chess club), I have provided a "guide" of sorts to walk you through testing certain features.

# `CRUD` like behaviors

Remember, to be able to perform `CRUD` like behaviors, you must be designated as `staff` or `superuser`. Thus, remember to login as either `cs50staff` or `cs50superuser.`

You can view the video where I test **some**, but **not all** features described below.
- https://youtu.be/1NetT8cF4eI

## 1. Create Classifications

Once you log in, please click on the "Classifications" link in the navbar. Again, this will only be available if you are a staff member or superuser.

You can then see the classification appear on the list of classifications. You can `view`, `edit`, `delete` the test one. Just make sure you add a few more classifications (at least 2). This way, you have multiple classifications to choose from when assigning players.

Note that if there are no classifications, then when trying to add a player, you will receive a warning that you cannot add a player until you have added classifications.

## 2. Create a Club

This is simple, just click the `Create Club!` button below the clubs player (accessed by clicking the `Home (Clubs)` link at the top of the navbar).

This will redirect you back to the `/clubs` route where a table of the clubs are there.

## 3. Add Players

You can add a few players. You can do this by clicking the `Add Player` button next to the `club` that you want to create one for. (You should have been redirected to the `/clubs` table after adding a club. If not, you can just click the `Home (Clubs)` link in the navbar.

I would recommend adding at least three players, as processing games between two players is not that interesting. With three, you could have more combinations, such as `Player 1` beating `Player 2` but losing to `Player 3`.

I would also recommend changing the `rating` field for each player. They default to 1200, but ratings are processed differently depending on the difference in rating between players, so that would be interesting to see here.

The mandatory fields are marked with an asterisk. There are two forms of authentication, one with Bootstrap JS and one with the backend.

Feel free to add as much information as you'd like.

When you add a player, you will be redirected to the players for the club that player is under. For example, if you created the player under `Club A`, then it will redirect you to the players table for `Club A`.

### Subtest - Auto-updating the UCSF ID

You can then immediately subtest to ensure that the app auto updates the UCSF Rating given a UCSF ID. You can click `Edit` for the player you just added, and then add a USCF ID. You can add my ID which is `13778174`.

Notice that once you click `Submit` it will process, update the ID and redirect you to the Players table, where you can see that the player's UCSF rating has been updated.

[Here](http://www.uschess.org/msa/thin.php?13778174) is the URL showing that that is indeed my USCF rating.

## 4. Add a few games
Again, to add a game, you must have created a club with at least two players in it. Again, it is more interesting when having three players.

To add a game, you can click the `Add Game` next to the `club` that you want to create one for. Again, you can click the `Home (Clubs)` link in the navbar to arrive at this table.

Play around as much as you'd like, entering different combinations of games for each player. Notice that when you add a game that if you go to the `View Players` route for the club, the `Number of Games` counter is automatically updated for each player.

Also notice that once you add at least one game, there will appear a `Process Games` button.

## 5. Process the games
This is the main part that will save the chess administrator a lot of time.

By default, when a game is created, it is marked as unprocessed. When there exists at least one unprocessed game in a club, then there will appear a `Process Games` button at the bottom of the games table.

Navigate to the `Games` table associated with the club you have been adding games too.

When you're ready, just click the `Process Games` button and follow through with the modal that pops up.

Hit the confirm, and the magic happens.
* All games are processed, and are now marked as processed. Notice that the `Process Games` button no longer appears
* Each game's `JSON` field will be populated with a `JSON` object containing information about the black and white players (their `ID`, `differential`, and their `rating_before`)
* Each game is also assigned a batch number. A batch is currently not being used for anything right now, but can be used in the future to step back in time and revert changes. But for now, when unprocessed games are processed, a batch is created.
  * A huge JSON object is created with:
    * A list of the IDs of the games that were just processed
    * An object of player `ID`s that contain three pieces of information (`rating_before`, `differential`, `rating_after`)
  * A `processed_on` date is automatically added. This will be useful when stepping back in time. Let's say a lost game is found but the games on that date have been processed. Some time down the road, I'd like to implement something where all games going back to that point are "unprocessed" (ratings also updated), the game is added, and then everything is processed again until that point.
  * The large amount of data stored is just to ensure that I would have everything I need when building out additional features.
  * You can view the batch by going back to the `clubs` table (click the `Home (Clubs)` link in the navbar) and clicking the `View Batches` button associated with the desired club.

# Differentiating User Roles

As I said before, there are three main roles:
* `Non-staff` - use the `cs50` username
* `Staff` - use the `cs50staff` username
* `Superuser` - use the `cs50superuser` username

All passwords are `cs50rocks!`

## 1. Testing `non-staff`
As you have already seen all the editing power that you have as a `staff` or `superuser`, I will not have you walk through it again. Just notice that you have buttons such as `Add Game`, `Add Player`, `View Batches`.

If you logout and login as just a `non-staff`, notice a few changes:
* You only see `View Games` and `View Players` buttons
* If you go to the `/classifications` table, you don't see the `View`, `Edit`, or `Delete` buttons.
* You don't see the link to the `Admin` page at the top right corner. (Note that you would also not have seen this if you logged in previously as `staff`.

## 2. Testing `superuser`
As discussed, only the `superuser` will have privileges to the admin site.

If you logout and login with the username `cs50superuser`, you would see an `Admin` link appear at the top right of the navbar.

If you click this, the `Admin` page will open in a new tab.

Here, you can perform a few features:
* All `CRUD` operations can be performed by clicking on the model that you want to add a record for
* Filter records for models pretty extensively.
  * For games, you can filter by `Club` and `Batch ID`
  * For batches, you can filter by `Processed On` date, which may not be testable by you because those are automatically generated.
  * For players, there is extensive filtering. You can filter by `Club`, `Classification`, `Grade`, and `Is Active?` (this is not as relevant now, but later on, players may leave club for a semester and thus be not active but we want to keep their record in case they come back. This can be done manually right now. No logic has been implemented for gating these players out as of yet.)
* Create a new user, say `staff`.

### Subtest for `superuser` - creating a new user
1. Click on the `Home` breadcrumb at the top of the page.
2. Click on `+Add` next to `Users`
3. Then click on `Add User +` on the right side of the page.
4. Fill out the information and click `Save`
5. To edit the privileges of a user (ex. promoting them to staff), click on the user in the user table.
  * Scroll down to `Permissions`
  * Check the `Staff Status` box. You can also promote to superuser if desired.
  * Then click `Save`

### Subtest - Password Reset
Please click the `Forgot Password` link. I have linked the `cs50superuser` account with `sarim.abbas@yale.edu`. You should be able to get a password reset for the account there.
