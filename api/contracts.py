from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct
import os
from dotenv import load_dotenv
load_dotenv()
from .abi.erc20_abi_file import erc20_abi
from .abi.erc721_abi_file import erc721_abi
from .abi.marketplace_abi_file import marketplace_abi


class contract_ERC20():
    def __init__(self, contract_address):
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('RPC_PROVIDER')))
        contract_address = Web3.to_checksum_address(contract_address)
        contract_abi = erc20_abi
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
    
    def mint(self, account_address, amount, private_key_signer):
        try:
            sender_account_address = self.web3.eth.account.from_key(private_key_signer).address
            transaction_data = self.contract.functions.mint(account_address, self.web3.to_wei(amount, 'ether')).build_transaction({
                'from': sender_account_address,
                'gas': int(os.getenv('GAS')),
                'gasPrice': self.web3.to_wei(int(os.getenv('GAS_PRICE')), 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(sender_account_address)
            })
            print(transaction_data)
            signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, private_key_signer)
            transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            return transaction_hash.hex()
        except:
            return False
    def transfer(self, account_address, amount, private_key_signer):
        try:
            sender_account_address = self.web3.eth.account.from_key(private_key_signer).address
            transaction_data = self.contract.functions.transferFrom(sender_account_address, account_address, self.web3.to_wei(amount, 'ether')).build_transaction({
                'from': sender_account_address,
                'gas': int(os.getenv('GAS')),
                'gasPrice': self.web3.to_wei(int(os.getenv('GAS_PRICE')), 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(sender_account_address)
            })
            signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, private_key_signer)
            #transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            return signed_transaction.rawTransaction
        except:
            return False
    def allow(self, spender_address, amount, private_key_signer):
        try:
            sender_account_address = self.web3.eth.account.from_key(private_key_signer).address
            transaction_data = self.contract.functions.approve(Web3.to_checksum_address(spender_address), int(amount)).build_transaction({
                'from': sender_account_address,
                'gas': int(os.getenv('GAS')),
                'gasPrice': self.web3.to_wei(int(os.getenv('GAS_PRICE')), 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(sender_account_address)
            })
            signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, private_key_signer)
            transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            return transaction_hash
        except:
            return False
        
class contract_ERC721():
    def __init__(self, contract_address):
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('RPC_PROVIDER')))
        contract_address = Web3.to_checksum_address(contract_address)
        contract_abi = erc721_abi
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)
    
    def validate_ownership(self, id, private_key_signer):
        try:
            sender_account_address = self.web3.eth.account.from_key(private_key_signer).address
            return self.contract.caller().ownerOf(id) == sender_account_address
        except:
            return False
    def transfer(self, account_address, id, private_key_signer):
        try:
            sender_account_address = self.web3.eth.account.from_key(private_key_signer).address
            transaction_data = self.contract.functions.transferFrom(sender_account_address, Web3.to_checksum_address(account_address), id).build_transaction({
                'from': sender_account_address,
                'gas': int(os.getenv('GAS')),
                'gasPrice': self.web3.to_wei(int(os.getenv('GAS_PRICE')), 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(sender_account_address)
            })
            signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, private_key_signer)
            #transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            return signed_transaction.rawTransaction
        except:
            return False
        
    def allow(self, spender_address, token_id, private_key_signer):
        try:
            sender_account_address = self.web3.eth.account.from_key(private_key_signer).address
            transaction_data = self.contract.functions.approve(Web3.to_checksum_address(spender_address), token_id).build_transaction({
                'from': sender_account_address,
                'gas': int(os.getenv('GAS')),
                'gasPrice': self.web3.to_wei(int(os.getenv('GAS_PRICE')), 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(sender_account_address)
            })
            signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, private_key_signer)
            transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            return transaction_hash
        except:
            return False
        
class contract_marketplace():
    def __init__(self, contract_address):
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('RPC_PROVIDER')))
        contract_address = Web3.to_checksum_address(contract_address)
        contract_abi = marketplace_abi
        self.contract = self.web3.eth.contract(address=contract_address, abi=contract_abi)

    def finish(self, auction_data, buyer_sign, seller_sign):
        try:
            sender_account_address = self.web3.eth.account.from_key(os.getenv('PRIVATE_KEY')).address
            transaction_data = self.contract.functions.finishAuction(auction_data, buyer_sign, seller_sign).build_transaction({
                'from': sender_account_address,
                'gas': int(os.getenv('GAS')),
                'gasPrice': self.web3.to_wei(int(os.getenv('GAS_PRICE')), 'gwei'),
                'nonce': self.web3.eth.get_transaction_count(sender_account_address)
            })
            signed_transaction = self.web3.eth.account.sign_transaction(transaction_data, os.getenv('PRIVATE_KEY'))
            transaction_hash = self.web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
            print("txn:", transaction_hash.hex())
            return transaction_hash
        except:
            return False
    
    def sign_buyer(self, erc20_address, erc721_address, token_id, amount_bid, private_key):
        auction_data = {
            'collectionAddress': erc721_address,
            'erc20Address': erc20_address,
            'tokenId': token_id,
            'bid': amount_bid
        }
        message = Web3.solidity_keccak(
            ['address', 'address', 'uint256', 'uint256'],
            [Web3.to_checksum_address(auction_data['collectionAddress']), Web3.to_checksum_address(auction_data['erc20Address']), auction_data['tokenId'], auction_data['bid']]
        ).hex()
        signed_message = Account.sign_message(encode_defunct(hexstr=message), private_key)
        signature = signed_message.signature.hex()
        return signature
    
    def sign_seller(self, buyer_sign, private_key):
        hash = Web3.keccak(hexstr=buyer_sign)
        signature = Account.sign_message(encode_defunct(hexstr=hash.hex()), private_key).signature.hex()
        return signature

        
class utils_web3():
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('RPC_PROVIDER')))

    def get_address_from_private_key(self, private_key):
        return self.web3.eth.account.from_key(private_key).address
    
    def eth_to_wei(self, amount):
        return self.web3.to_wei(int(amount),'ether')
    
    def hex_byte_parse(self, string):
        print(string)
        return self.web3.eth.transactions.Transaction(hexstr=string)