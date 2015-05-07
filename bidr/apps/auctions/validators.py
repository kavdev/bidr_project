"""
.. module:: bidr.apps.auctions.validators
   :synopsis: Bidr Silent Auction System Auction Validators.

.. moduleauthor:: Jarred Stelfox <>

"""
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


def validate_user_exists(email):
    """
    This validates that a user exists in the database.

    :raises: **ValidationError** if the user does not exist.

    """

    if not get_user_model().objects.filter(email=email).exists():
        raise ValidationError("User provide does not exist!")
