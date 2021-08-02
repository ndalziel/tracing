from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash #the tx_hash on the Bitcoin blockchain
        self.n = n #the position of this output in the transaction
        self.amount = amount #the value of this transaction output (in Satoshi)
        self.owner = owner #the Bitcoin address of the owner of this output
        self.time = time #the time of this transaction as a datetime object
        self.inputs = [] # a list of TXO objects

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
    
        tx = rpc_connection.getrawtransaction(tx_hash,True)
        tx_details = tx['vout'][0]

        hash = tx_hash
        n = tx_details['n']
        amount = int(tx_details['value']) *100000000
        time = datetime.fromtimestamp(tx['time'])
        owner =  tx_details['scriptPubKey']['hex']
        return cls(hash,n,amount, owner, time)

    def get_inputs(self,d=1):
    
        # Connects to the Bitcoin blockchain, and populate the list of inputs, up to a depth d
        # In other words, if   d=1  it should create TXO objects to populate self.inputs with the appropriate TXO objects. 
        # If d=2  it should also populate the inputs field of each of the TXOs in self.inputs etc.

        tx_inputs = rpc_connection.getrawtransaction(self.tx_hash,True)['vin']
        for tx in tx_inputs:
            txo = TXO.from_tx_hash(tx['txid'])    
            self.inputs.append(txo)
            if d>1:
                txo.get_inputs(d-1)
        return  tx_inputs