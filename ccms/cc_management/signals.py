from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *

from requests_html import HTMLSession

BASE_URL = "http://www.uschess.org/msa/thin.php?"

@receiver(post_save, sender=Player)
def update_uscf(sender, instance, raw, **kwargs):

    # If nothing, return
    if not instance:
        return

    # Get the USCF ID
    uscf_id = instance.uscf_id

    # Check if it's currently being processed
    if hasattr(instance, '_rating_processed'):
        return

    # Query the URL and get the rating
    session = HTMLSession()
    if uscf_id:
        response = session.get(BASE_URL + str(uscf_id))
        if response:
            rating_input = response.html.find("input[name=rating1]", first=True)
            rating_value_string = rating_input.attrs["value"]
            rating_value = int(rating_value_string[:rating_value_string.find("*")])
            instance.uscf_rating = rating_value

    # Save the instance
    try:
        instance._rating_processed = True
        instance.save()
    # Remove the instance so no infinite recursion
    finally:
        del instance._rating_processed
