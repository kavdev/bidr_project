"""
.. module:: bidr.apps.items.models
   :synopsis: Bidr Silent Auction System Item Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>
.. moduleauthor:: Zachary Glazer <glazed4@yahoo.com>

"""

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator
from django.db.models.aggregates import Max, Sum
from django.db.models.fields import CharField, TextField, BigIntegerField, BooleanField
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from polymorphic.models import PolymorphicModel
from taggit.managers import TaggableManager

from ..bids.models import Bid


class AbstractItem(PolymorphicModel):
    """ Abstract class for Items """

    name = CharField(max_length=60)
    description = TextField(blank=True, max_length=300)
    claimed = BooleanField(default=False)
    claimed_bid = ForeignKey(Bid, null=True, blank=True, verbose_name="Claimed Bid")
    bids = ManyToManyField(Bid, blank=True, related_name="bids", verbose_name="Bids")

    def claim(self, bid):
        self.claimed = True
        self.claimed_bid = bid
        self.save()

    def get_second_highest_bid(self):
        bid_list = self.get_bids_by_amount()
        if bid_list.count() > 1:
            return bid_list[1]
        else:
            return None

    def get_previous_bid_by_user(self, user):
        bid_list = self.bids.filter(user=user).order_by("-amount")

        if bid_list.count() > 1:
            return bid_list[1]

    def __str__(self):
        return self.name

    def get_bids_by_amount(self):
        return self.bids.all().order_by("-amount")

    @property
    def image_urls(self):
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def highest_bid(self):
        """ This only works because no bid can have the same amount."""

        highest_amount = self.bids.all().aggregate(Max('amount'))["amount__max"]
        if not highest_amount:
            return None
        return self.bids.get(amount=highest_amount)

    @property
    def total_starting_bid(self):
        raise NotImplementedError("Subclasses should implement this!")

    @property
    def polymorphic_identifier(self):
        return self.polymorphic_ctype.name

    @property
    def bidders(self):
        bidders = []
        [bidders.append(bid.user) for bid in self.bids.all()]
        return list(set(bidders))

    @property
    def highest_bid_for_each_bidder(self):
        bidrs = self.bidders
        highest_bids = []
        [highest_bids.append(self.get_highest_bid_of_bidder(bidr)) for bidr in bidrs]
        return highest_bids

    def get_highest_bid_of_bidder(self, bidder):
        bids = self.bids.all().filter(user=bidder)
        highest_amount = bids.all().aggregate(Max('amount'))["amount__max"]
        if not highest_amount:
            return None
        return bids.get(amount=highest_amount)

    def get_absolute_client_url(self, request):
        auction_id = self.bidables.all()[0].id
        return request.build_absolute_uri(
            reverse("client:item_detail", kwargs={"auction_id": auction_id, "pk": self.id})
        )


class Item(AbstractItem):
    """ An auction item."""

    starting_bid = BigIntegerField(default=0, validators=[MinValueValidator(0)])
    picture = ImageField(null=True, blank=True)

    tags = TaggableManager()

    def _image_url(self):
        if self.picture:
            return self.picture.url
        else:
            return static('img/no_image.png')

    @property
    def image_urls(self):
        return [self._image_url()]

    @property
    def total_starting_bid(self):
        return self.starting_bid


class ItemCollection(AbstractItem):
    """ A collection of items."""

    items = ManyToManyField(Item, blank=True, verbose_name="Items")

# @glazed4444 Not sure why this is here. Items are no longer biddables once they're in a collection
#     def claim(self, bid):
#         for item in self.items.all():
#             item.claim(bid)
#         super(ItemCollection, self).claim(bid)

    @property
    def image_urls(self):
        return [x._image_url() for x in self.items.all()[:4]]

    @property
    def total_starting_bid(self):
        return self.items.aggregate(Sum('starting_bid'))["starting_bid__sum"]

    @property
    def ordered_items(self):
        return self.items.all().order_by("name")

    @property
    def tags(self):
        tag_set = set()
        # List compression syntax is not python's strongsuit...
        [tag_set.add(tag) for item in self.items.all() for tag in item.tags.names()]

        return list(tag_set)
