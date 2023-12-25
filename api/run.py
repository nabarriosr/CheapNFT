from eth_account import Account
from web3 import Web3

# Dirección y clave privada de la cuenta que realizará la firma
account_address = '0xCf05ca5D83b200369e932c34c0281057DbFaCF30'
private_key = '8f2a395a2bad0f9af0562009c832b07b851cda1923b0fb524834de35ac4f3742'

# Datos de la subasta
collection_address = '0xfce9b92ec11680898c7fe57c4ddcea83aeaba3ff'  # Dirección del contrato ERC721
collection_address = Web3.to_checksum_address(collection_address)
erc20_address = '0xbd65c58d6f46d5c682bf2f36306d461e3561c747'  # Dirección del contrato ERC20
erc20_address = Web3.to_checksum_address(erc20_address)
token_id = 238             # ID del token ERC721 en subasta
bid = 100000000000                    # Oferta en tokens ERC20


# Crear un objeto de datos de la subasta
auction_data = {
    'collectionAddress': collection_address,
    'erc20Address': erc20_address,
    'tokenId': token_id,
    'bid': bid
}

# Convertir los datos de la subasta a una cadena
message = Web3.solidity_keccak(
    ['address', 'address', 'uint256', 'uint256'],
    [auction_data['collectionAddress'], auction_data['erc20Address'], auction_data['tokenId'], auction_data['bid']]
).hex()

# Firmar el mensaje con la clave privada
private_key_bytes = bytes.fromhex(private_key)
signed_message = Account.sign_message(message, private_key_bytes)

# Obtener las firmas del postor y del propietario
bidder_signature = signed_message.signature.hex()
owner_signature = signed_message.signature.hex()  # Esto es solo un ejemplo; deberías obtener una firma diferente del propietario

# Conectar a un nodo de Ethereum (puede ser un nodo local o un servicio como Infura)
w3 = Web3(Web3.HTTPProvider('https://rpc2.sepolia.org/'))

# Dirección del contrato y ABI (Interfaz binaria del contrato)
contract_address = '0x597c9bc3f00a4df00f85e9334628f6cdf03a1184'  # Reemplaza con la dirección real del contrato
contract_abi = [
    {"inputs":[{"components":[{"internalType":"address","name":"collectionAddress","type":"address"},{"internalType":"address","name":"erc20Address","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"bid","type":"uint256"}],"internalType":"struct Marketplace.AuctionData","name":"auctionData","type":"tuple"},{"internalType":"bytes","name":"bidderSig","type":"bytes"},{"internalType":"bytes","name":"ownerApprovedSig","type":"bytes"}],"name":"finishAuction","outputs":[],"stateMutability":"nonpayable","type":"function"}
]  # Reemplaza con el ABI real del contrato

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
