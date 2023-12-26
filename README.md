# CHEAP NFT

## Requisites

Python, Django and REST FRAMEWORK

## Run

Please edit .env file with a private key for the Marketplace wallet

```shell
Execute these commands on teh root folder
python3 -m virtualenv venv
source venv/bin/activate
python3 manage.py flush
python3 manage.py migrate --run-syncdb
python3 manage.py createsuperuser
python3 manage.py runserver

```
And answer with your own user admin info

## Postman

Import the collection located on the root in your envirionment of postman, and fill the body parameters with your tests arguments


## Scenarios 

Review POSTMAN colelction and the diagram on that folder ./postman to better understanding

### Purchase ERC20

Use the endpoint http://localhost:8000/api/erc20-purchase with a POST request to mint tokens erc0 to your wallet

### Fix Price

(At any moment go to http://localhost:8000/api/bids/ to review the state of your process on the local database)

Owner: Original owner of NFT
Bidder: Buyer of the NFT

- Owner: First at all, you must generate your NFT, for example using the etherscan from your metamask, and get the count of NFT to get the nft_id of yur assets
- Owner: Use the endpoint http://localhost:8000/api/publish_offer with a POST request to publish your NFT using your private key, this will be saved on the database and launch the tarnsaction to allow access to transfer ERC721 token for marketplace smart contract.
- Bidder: Use the endpoint http://localhost:8000/api/accept_offer with a POST request to accept the offer of the owner, reviewing the database you can get the id of the process, and with your private key generate the bidder signature, additionally launch the tarnsaction to allow access to transfer ERC20 token for marketplace smart contract.
- Owner: Use the endpoint http://localhost:8000/api/accept_offer with a POST request to finsih the process, generating the ownerSignature and launch the transaction finishAUction to end the process.


### Auction

(At any moment go to http://localhost:8000/api/bids/ to review the state of your process on the local database)

Owner: Original owner of NFT
Bidder: Buyer of the NFT

- Owner: First at all, you must generate your NFT, for example using the etherscan from your metamask, and get the count of NFT to get the nft_id of yur assets
- Owner: Use the endpoint http://localhost:8000/api/publish_offer with a POST request to publish your NFT using your private key, this will be saved on the database and launch the tarnsaction to allow access to transfer ERC721 token for marketplace smart contract.
- Bidder: Use the endpoint http://localhost:8000/api/accept_offer with a POST request to accept create and offer for the owner, reviewing the database you can get the id of the process, and with your private key generate the bidder signature, additionally launch the tarnsaction to allow access to transfer ERC20 token for marketplace smart contract.
- Bidder: The last step can be repeated before the owner finish the auction if the request offer a higher price.
- Owner: Use the endpoint http://localhost:8000/api/accept_offer with a POST request to finsih the process, generating the ownerSignature and launch teh tarnsaction finishAUction to end teh process.



## COMMENTS:

- The private key is being sent on the api, but in production this is not safe, the usual is a custody on backend or some inetractions from the FE using metamask or local client PK, but for teh excercise works.
- When a bidder launch a higher offer, doesnt exist a log to see hysitory, but that refinements are not neccesary for the purpose of this excercise
- A possible customization is stablish a price of gas customized from the API where the user can choice a rate respect to the average price of gas on the network, for purposes of this repo that variables are fixed on file .env
- This transaction was executed from this repo https://sepolia.etherscan.io/tx/0x6646dbd90fc7021c3584d54ea5c0e399efda3b66a2fc504b9265ecf8529a5617
