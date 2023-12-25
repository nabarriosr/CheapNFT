from eth_account import Account
from eth_abi import encode
from web3 import Web3
from eth_account.messages import encode_defunct
#from .abi.hasher_abi_file import hasher_abi

hasher_abi = [
    {"inputs": [{"components": [{"internalType": "address","name": "collectionAddress","type": "address"},{"internalType": "address","name": "erc20Address","type": "address"},{"internalType": "uint256","name": "tokenId","type": "uint256"},{"internalType": "uint256","name": "bid","type": "uint256"}],"internalType": "struct Hasher.AuctionData","name": "auctionData","type": "tuple"}],"name": "hash","outputs": [{"internalType": "bytes32","name": "","type": "bytes32"}],"stateMutability": "pure","type": "function"}
]

# Dirección y clave privada de la cuenta que realizará la firma
account_address = '0xCf05ca5D83b200369e932c34c0281057DbFaCF30'
private_key = '8f2a395a2bad0f9af0562009c832b07b851cda1923b0fb524834de35ac4f3742'



hasher_address = Web3.to_checksum_address("0xBdb1c36e66A997a8DA6531915D432E135A2a3882")
hasher_contract_abi = hasher_abi
web3 = Web3(Web3.HTTPProvider("https://rpc2.sepolia.org/"))
hasher_contract = web3.eth.contract(address=hasher_address, abi=hasher_contract_abi)



# Datos de la subasta
collection_address = Web3.to_checksum_address('0xfce9b92ec11680898c7fe57c4ddcea83aeaba3ff') # Dirección del contrato ERC721
erc20_address = Web3.to_checksum_address('0xbd65c58d6f46d5c682bf2f36306d461e3561c747')       # Dirección del contrato ERC20
token_id = 238                # ID del token ERC721 en subasta
bid = 1000000000000000000                     # Oferta en tokens ERC20

print(collection_address)
print(erc20_address)
# Crear un objeto de datos de la subasta
auction_data = {
    'collectionAddress': collection_address,
    'erc20Address': erc20_address,
    'tokenId': token_id,
    'bid': bid
}


private_key_signer = "8f2a395a2bad0f9af0562009c832b07b851cda1923b0fb524834de35ac4f3742"
sender_account_address = web3.eth.account.from_key(private_key_signer).address
result = hasher_contract.caller().hash(auction_data)


# Calcular el hash keccak256
#message_hash = Web3.solidity_keccak(packed_data1, packed_data2)

print("message_hash:", result.hex())


# Convertir los datos de la subasta a una cadena
message = Web3.solidity_keccak(
    ['address', 'address', 'uint256', 'uint256'],
    [Web3.to_checksum_address(auction_data['collectionAddress']), Web3.to_checksum_address(auction_data['erc20Address']), auction_data['tokenId'], auction_data['bid']]
).hex()


print("Hash Bidder:", message)


signed = Account.sign_message(encode_defunct(hexstr=message), 'e5d2415ed25948994de242cae4d89543c3a3c2d363a86cc2a8ce1791b6f34fb0')
print("BIDDER SIGN: ", signed.signature.hex())



signed2 = Web3.keccak(hexstr=signed.signature.hex())

print("Hash Owner:", signed2.hex())


print("OWNER SIGN: ", Account.sign_message(encode_defunct(hexstr=signed2.hex()), private_key).signature.hex())



'''
# Supongamos que auctionData es un objeto con los atributos mencionados
auctionData = {
    'collectionAddress': '0x1234567890123456789012345678901234567890',
    'erc20Address': '0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef',
    'tokenId': 123,
    'bid': 456
}

# Codificar los parámetros usando abi.encodePacked
packed_data = encode_abi(['address', 'address', 'uint256', 'uint256'],
                         [Web3.toChecksumAddress(auctionData['collectionAddress']),
                          Web3.toChecksumAddress(auctionData['erc20Address']),
                          auctionData['tokenId'],
                          auctionData['bid']])

# Calcular el hash keccak256
message_hash = Web3.keccak(packed_data)

print("message_hash:", message_hash.hex())

'''
'''

# Firmar el mensaje con la clave privada
private_key_bytes = bytes.fromhex(private_key)
signed_message = Account.sign_message(message, private_key_bytes)

# Obtener las firmas del postor y del propietario
bidder_signature = signed_message.signature.hex()
owner_signature = signed_message.signature.hex()  # Esto es solo un ejemplo; deberías obtener una firma diferente del propietario

# Conectar a un nodo de Ethereum (puede ser un nodo local o un servicio como Infura)
w3 = Web3(Web3.HTTPProvider('tu_url_del_nodo_ethereum'))

# Dirección del contrato y ABI (Interfaz binaria del contrato)
contract_address = '0x...'  # Reemplaza con la dirección real del contrato
contract_abi = [...]  # Reemplaza con el ABI real del contrato

# Crear instancia del contrato
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Llamar a la función finishAuction
transaction = contract.functions.finishAuction(auction_data, bidder_signature, owner_signature).buildTransaction({
    'from': account_address,
    'gas': 2000000,  # Ajusta la cantidad de gas según sea necesario
    'gasPrice': w3.toWei('50', 'gwei'),  # Ajusta el precio del gas según sea necesario
    'nonce': w3.eth.getTransactionCount(account_address),
})

# Firmar la transacción con la clave privada
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

# Enviar la transacción
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
print('Transacción enviada. Hash:', tx_hash.hex())
'''