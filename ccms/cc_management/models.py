from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=100)
    # Define how it's displayed
    def __str__(self):
        return self.name

# These are the classifications for a club
# Ex. Pawns, Knights, Bishops, Rooks
class Club_Classifications(models.Model):
    name = models.CharField(max_length=100)
    # Define how it's displayed
    def __str__(self):
        return self.name

# Player Model
class Player(models.Model):
    # Club ID
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="Club Name")

    # Classficiation, default is 1, which is pawns
    classification = models.ForeignKey(Club_Classifications, on_delete=models.CASCADE, default=1)

    # Created at and Updated at fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=100, verbose_name="First Name")
    # Middle Names are optional
    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Middle Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")

    # USCF is optional
    uscf_id = models.IntegerField(blank=True, null=True, verbose_name="USCF ID")
    uscf_rating = models.IntegerField(blank=True, null=True, verbose_name="USCF Rating")
    # Rating is mandatory, default 0
    rating = models.IntegerField(default=0, verbose_name="Club Rating")
    # Number of games is mandatory, default 0
    games_played = models.IntegerField(default=0, verbose_name="# of Games Played")

    # Players can be made inactive
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")

    # Grade is mandatory
    KINDERGARTEN = 0
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10
    ELEVENTH = 11
    TWELFTH = 12
    GRADE_CHOICES = (
        (KINDERGARTEN, 'Kintergarten'),
        (FIRST, '1st'),
        (SECOND, '2nd'),
        (THIRD, '3rd'),
        (FOURTH, '4th'),
        (FIFTH, '5th'),
        (SIXTH, '6th'),
        (SEVENTH, '7th'),
        (EIGHTH, '8th'),
        (NINTH, '9th'),
        (TENTH, '10th'),
        (ELEVENTH, '11th'),
        (TWELFTH, '12th'),
    )
    grade = models.IntegerField(choices=GRADE_CHOICES, blank=True, null=True)

    # This is so that when people select things from dropdown, they see the player name
    # 
    def __str__(self):
        return self.first_name + " " + self.last_name
    # TODO - Can classify people by elementary, middle
    """
    def is_upperclass(self):
        return self.year_in_school in (self.JUNIOR, self.SENIOR)
    """

# Game Model
class Game(models.Model):
    # Club ID
    club = models.ForeignKey(Club, on_delete=models.CASCADE, verbose_name="Club Name")

    # Created at and Updated at fields
    # Use played_on instead of created_at
    played_on = models.DateField(auto_now_add=True, verbose_name="Played On")
    updated_at = models.DateField(auto_now=True)

    # Batch ID
    batch_id = models.IntegerField(blank=True, null=True, verbose_name="Batch Number")

    # Player IDs
    black_player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="Black Player", related_name="black_player")
    white_player = models.ForeignKey(Player, on_delete=models.CASCADE, verbose_name="White Player", related_name="white_player")

    # Results
    BLACK = 0
    DRAW = 1
    WHITE = 2

    # Grade is mandatory
    GAME_RESULTS = (
        (BLACK, 'Black Won!'),
        (DRAW, 'Draw!'),
        (WHITE, 'White Won!')
    )
    result = models.IntegerField(choices=GAME_RESULTS, verbose_name="Result")

    # Processed is false by detault
    processed = models.BooleanField(default=False, verbose_name="Processed?")

    # JSON column
    json = JSONField(blank=True, null=True)
