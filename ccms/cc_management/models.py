from django.db import models

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
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)

    # Classficiation, default is 1, which is pawns
    classification = models.ForeignKey(Club_Classifications, on_delete=models.CASCADE, default=1)

    # Created at and Updated at fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=100)
    # Middle Names are optional
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)

    # USCF is optional
    uscf_id = models.IntegerField(blank=True, null=True)
    uscf_rating = models.IntegerField(blank=True, null=True)
    # Rating is mandatory, default 0
    rating = models.IntegerField(default=0)
    # Number of games is mandatory, default 0
    games_played = models.IntegerField(default=0)

    # Players can be made inactive
    is_active = models.BooleanField(default=True)

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

    # TODO - Can classify people by elementary, middle
    """
    def is_upperclass(self):
        return self.year_in_school in (self.JUNIOR, self.SENIOR)
    """