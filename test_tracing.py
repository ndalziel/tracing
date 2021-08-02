from trace_txes import *
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))
block_hash = rpc_connection.getblockhash(110000)   
tx_hash = rpc_connection.getblock(block_hash)['tx'][1]

txo = TXO.from_tx_hash(tx_hash)    
print(txo.time)
txo.get_inputs(2)
print(txo.inputs[0].time)
print(txo.inputs[0].inputs[0].time)
#next_txo.get_inputs()
#print (next_txo.inputs[0])



