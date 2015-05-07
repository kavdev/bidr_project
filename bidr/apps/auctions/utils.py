"""
.. module:: bidr.apps.auctions.utils
   :synopsis: Bidr Silent Auction System Auction Utilities.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from ..auctions.models import STAGES


def _end_auction(auction):
    """
    End an auction if it hasn't already ended. If all items are claimed or not claimed,
    the stage skips to report.
    """

    if auction.stage < STAGES.index("Claim"):
        unclaimed_items = auction.bidables.filter(claimed=False).exclude(bids=None)

        if not unclaimed_items:
            auction.stage = STAGES.index("Report")
        else:
            auction.stage = STAGES.index("Claim")

        auction.save()

    return auction.stage
