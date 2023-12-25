from rest_framework import viewsets
from .serializer import BidSerializer
from django.http import JsonResponse
from .models import Bid
from .contracts import contract_ERC20
from .contracts import contract_ERC721
from .contracts import contract_marketplace
from .contracts import utils_web3
import os
from dotenv import load_dotenv
load_dotenv()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
from web3 import Web3


 


utils_web3_class = utils_web3()

class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer



def ERC20Purchase(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        account_address = request.POST.get('address')
        contract = contract_ERC20(os.getenv('ERC20_CONTRACT_ADDRESS'))
        data = contract.mint(account_address, int(amount), os.getenv('PRIVATE_KEY'))
        if(data == False):
            code = False
        else:
            code = "OK"
        return JsonResponse({"data": data, "code": code})



def PublishOffer(request):
    utils_web3_class = utils_web3()
    try:
        data = False
        code = False
        if request.method == 'POST':
            contract = contract_ERC721(os.getenv('ERC721_CONTRACT_ADDRESS'))
            seller_address = utils_web3_class.get_address_from_private_key(request.POST.get('private_key'))
            nft_id = int(request.POST.get('nft_id'))
            validate_ownership =  contract.validate_ownership(nft_id, request.POST.get('private_key'))
            bytes_cero = b'\x00'
            if(validate_ownership):
                data_bid = {"seller_address":seller_address,"seller_sign":bytes_cero.hex(),"buyer_address":"0x0","buyer_sign":bytes_cero.hex(),"nft_id":nft_id,"price":int(request.POST.get('price')),"timestamp_publish": int(round(time.time())),"timestamp_close":0,"status":"offer-launch","ready":False}
                contract.allow(os.getenv('MARKETPLACE_CONTRACT_ADDRESS'), nft_id, request.POST.get('private_key'))
                serializer = BidSerializer(data=data_bid)
                if serializer.is_valid():
                    serializer.save()
                    data = "Saved"
                    code = "OK"
                print(data_bid)
            else:
                data = "It's not your NFT"
            return JsonResponse({"data": data, "code": code})
    except:
        return JsonResponse({"data": data, "code": code})
    

def PublishAuction(request):
    try:
        data = False
        code = False
        if request.method == 'POST':
            contract = contract_ERC721(os.getenv('ERC721_CONTRACT_ADDRESS'))
            seller_address = utils_web3_class.get_address_from_private_key(request.POST.get('private_key'))
            nft_id = int(request.POST.get('nft_id'))
            validate_ownership =  contract.validate_ownership(nft_id, request.POST.get('private_key'))
            bytes_cero = b'\x00'
            if(validate_ownership):
                data_bid = {"seller_address":seller_address,"seller_sign":bytes_cero.hex(),"buyer_address":"0x0","buyer_sign":bytes_cero.hex(),"nft_id":nft_id,"price":0,"timestamp_publish": int(round(time.time())),"timestamp_close":0,"status":"auction-launch","ready":False}
                contract.allow(os.getenv('MARKETPLACE_CONTRACT_ADDRESS'), nft_id, request.POST.get('private_key'))
                serializer = BidSerializer(data=data_bid)
                if serializer.is_valid():
                    serializer.save()
                    data = "Saved"
                    code = "OK"
                print(data_bid)
            else:
                data = "It's not your NFT"
            return JsonResponse({"data": data, "code": code})
    except:
        return JsonResponse({"data": data, "code": code})
    
def AcceptOffer(request):
    data = False
    code = False
    try:
        buyer_address = utils_web3_class.get_address_from_private_key(request.POST.get('private_key'))
        id=int(request.POST.get('id'))
        object = Bid.objects.get(pk=id)
        data_bid = BidSerializer(object).data
        nft_id = int(data_bid['nft_id'])
        if(data_bid['status']=='offer-launch'):
            '''
            contract = contract_ERC20(os.getenv('ERC20_CONTRACT_ADDRESS'))
            data_sign = contract.transfer(data_bid['seller_address'] ,data_bid["price"],request.POST.get('private_key'))
            
            data_bid['buyer_sign']=data_sign.hex()
            '''
            contract = contract_marketplace(os.getenv('MARKETPLACE_CONTRACT_ADDRESS'))
            data_bid['buyer_sign'] = contract.sign_buyer(os.getenv('ERC20_CONTRACT_ADDRESS'), os.getenv('ERC721_CONTRACT_ADDRESS'), nft_id, data_bid["price"], request.POST.get('private_key'))
            data_bid['buyer_address'] = buyer_address
            data_bid['status']='offer-accepted'
            
            serializer = BidSerializer(object, data=data_bid)
            if serializer.is_valid():
                contract_ERC20_class = contract_ERC20(os.getenv('ERC20_CONTRACT_ADDRESS'))
                contract_ERC20_class.allow(os.getenv('ERC20_CONTRACT_ADDRESS'), int(data_bid['price']), request.POST.get('private_key'))
                serializer.save()
                data = "Saved"
                code = "OK"
            print(data_bid)
        else:
            data = "Wrong status"
    except:
        print('Error')
    return JsonResponse({"data": data, "code": code})

def OfferAuction(request):
    data = False
    code = False
    try:
        buyer_address = utils_web3_class.get_address_from_private_key(request.POST.get('private_key'))
        id=int(request.POST.get('id'))
        object = Bid.objects.get(pk=id)
        data_bid = BidSerializer(object).data
        if(data_bid['status']=='auction-launch' or data_bid['status']=='auction-offered'):
            new_price = int(request.POST.get('price'))
            nft_id = int(data_bid['nft_id'])
            if(data_bid['price'] < new_price):               
                contract = contract_marketplace(os.getenv('MARKETPLACE_CONTRACT_ADDRESS'))
                data_sign = contract.sign_buyer(os.getenv('ERC20_CONTRACT_ADDRESS'), os.getenv('ERC721_CONTRACT_ADDRESS'), nft_id, new_price, request.POST.get('private_key'))
                data_bid['buyer_sign'] = data_sign
                data_bid['buyer_address'] = buyer_address
                print(data_sign) 
                data_bid['buyer_sign']=data_sign
                data_bid['status']='auction-offered'
                data_bid['price']=new_price
                
                serializer = BidSerializer(object, data=data_bid)
                if serializer.is_valid():
                    print('Test')
                    contract_ERC20_class = contract_ERC20(os.getenv('ERC20_CONTRACT_ADDRESS'))
                    contract_ERC20_class.allow(os.getenv('ERC20_CONTRACT_ADDRESS'), int(data_bid['price']), request.POST.get('private_key'))
                    serializer.save()
                    data = "Saved"
                    code = "OK"
                print(data_bid)
            else:
                data = "Try again with a higher offer"
        else:
            data = "Wrong status"
    except:
        print('Error')
    return JsonResponse({"data": data, "code": code})


def Finish(request):
    data = False
    code = False
    try:
        id=int(request.POST.get('id'))
        object = Bid.objects.get(pk=id)
        data_bid = BidSerializer(object).data
        if(data_bid['status']=='offer-accepted' or data_bid['status']=='auction-offered'):
            nft_id = int(data_bid['nft_id'])
            contract_auction= contract_marketplace(os.getenv('MARKETPLACE_CONTRACT_ADDRESS'))
            seller_sign = contract_auction.sign_seller(data_bid['buyer_sign'], request.POST.get('private_key'))
            data_bid['seller_sign'] = seller_sign
            data_bid['ready']=True
            data_bid['timestamp_close']=int(round(time.time()))
            data_bid['status'] = 'closed'
            auction_data={
                "collectionAddress":Web3.to_checksum_address(os.getenv('ERC721_CONTRACT_ADDRESS')),
                "erc20Address": Web3.to_checksum_address(os.getenv('ERC20_CONTRACT_ADDRESS')),
                "tokenId":nft_id,
                "bid":int(data_bid['price'])
            }
            seller_sign_message = seller_sign
            buyer_sign_message= data_bid['buyer_sign']
            print(3456)
            data = contract_auction.finish(auction_data, buyer_sign_message, seller_sign_message)
            serializer = BidSerializer(object, data=data_bid)
            if serializer.is_valid():
                serializer.save()
                data = "Saved"
                code = "OK"
        else:
            data = "Wrong status"
    except:
        print('Error')
    return JsonResponse({"data": data, "code": code})
