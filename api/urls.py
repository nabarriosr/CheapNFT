from django.urls import path,include
from rest_framework import routers
from api import views
from django.views.decorators.csrf import csrf_exempt


router = routers.DefaultRouter()
router.register(r'bids',views.BidViewSet)


urlpatterns=[
    path('', include(router.urls)),
    path('erc20-purchase', csrf_exempt(views.ERC20Purchase), name= "ERC20Purchase"),
    path('publish_offer', csrf_exempt(views.PublishOffer), name= "PublishOffer"),
    path('publish_auction', csrf_exempt(views.PublishAuction), name= "PublishAuction"),
    path('accept_offer', csrf_exempt(views.AcceptOffer), name= "AcceptOffer"),
    path('offer_auction', csrf_exempt(views.OfferAuction), name= "OfferAuction"),
    path('finish', csrf_exempt(views.Finish), name= "Finish")
]