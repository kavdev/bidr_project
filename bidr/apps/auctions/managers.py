"""
.. module:: bidr.apps.auctions.managers
   :synopsis: Bidr Silent Auction System Auction Model Managers.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.contrib.auth.models import BaseUserManager
from django.db.models import Q


class ManageableAuctionManager(BaseUserManager):

    def managed_by(self, user):
        return super(ManageableAuctionManager, self).get_queryset().filter(
            Q(managers__in=[user]) | Q(auctions__owner=user)
        )
