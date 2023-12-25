from web3 import Web3, Account
from abi.erc20_abi_file import erc20_abi

web3 = Web3(Web3.HTTPProvider('https://rpc2.sepolia.org/'))
print(web3.is_connected())
#print(erc20_abi)
# Dirección del contrato y ABI


contract_address = '0xbd65c58d6f46d5c682bf2f36306d461e3561c747'
contract_address = Web3.to_checksum_address(contract_address)
contract_abi = erc20_abi  # Inserta aquí el ABI de tu contrato

# Crear una instancia del contrato
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


# Cuenta desde la que se enviará la transacción (debe tener suficientes fondos)
sender_address = '0xCf05ca5D83b200369e932c34c0281057DbFaCF30'
#sender_address = '0xabcdef1234567890abcdef1234567890abcdef12'
#private_key = '0x441f6a6fd07bd2fe55c1cb7a1605777b453f8158d23f07df9f51c83cfe06b2d5'  # La clave privada de la cuenta (asegúrate de mantenerla segura)
private_key = '8f2a395a2bad0f9af0562009c832b07b851cda1923b0fb524834de35ac4f3742'

# Crear una instancia del objeto Account para firmar la transacción
account = Account.from_key(private_key)

print(account.address)


# Interactuar con una función del contrato (por ejemplo, una función 'get' que devuelve un valor)
function_result = contract.caller().symbol()
print(function_result)

# Enviar una transacción a una función del contrato (por ejemplo, una función 'set' que modifica el estado)

transaction_data = contract.functions.mint(sender_address, web3.to_wei(10, 'ether')).build_transaction({
    'from': sender_address,
    'gas': 100000,
    'gasPrice': web3.to_wei(50, 'gwei'),
    'nonce': web3.eth.get_transaction_count(sender_address),
})

signed_transaction = web3.eth.account.sign_transaction(transaction_data, private_key)
transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(f'Transacción enviada. Hash: {transaction_hash}')



  '''
    try:
        if request.method == 'POST':
            contract = contract_ERC721(os.getenv('ERC721_CONTRACT_ADDRESS'))
            data = contract.validate_ownership(request.POST.get('nft_id'), request.POST.get('private_key'))
            if(data == False):
                code = False
            else:
                code = "OK"
            return JsonResponse({"data": data, "code": code})
        #objeto = BidFix.objects.get(pk=2).seller_address
        serializer = BidFixSerializer(data={"seller_address": "0xasdf","buyer_address": "0xzxcv", "nft_id":"3"})
        if serializer.is_valid():
            serializer.save()

    except:
        return JsonResponse({"data": data, "code": code})

    #nuevo_valor = request.data.get('nuevo_valor')
    '''
    '''
    if nuevo_valor is not None:
        objeto.nombre = nuevo_valor
        objeto.save()
        return Response({'mensaje': 'Valor modificado correctamente'}, status=status.HTTP_200_OK)
    else:
        return Response({'mensaje': 'El nuevo valor no fue proporcionado'}, status=status.HTTP_400_BAD_REQUEST)
    '''




    '''
    
    '''
#objeto = BidFix.objects.get(pk=2).seller_address