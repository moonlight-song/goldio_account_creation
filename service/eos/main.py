from requests import post
from eosiopy.eosioparams import EosioParams
from eosiopy.nodenetwork import NodeNetwork
from eosiopy.rawinputparams import RawinputParams

from .config import network_config
from .validation import validate_public_key, validate_account_name
from .utils import account_exists


class Network:

	def __init__(self):
		network_config.check_can_push_transactions()
		for key, value in network_config.__dict__:
			setattr(self, key, value)


	def create_account(self, account_name, active_key, owner_key=None):

		validate_public_key(active_key)
		if owner_key is None:
			owner_key = active_key
		else:
			validate_public_key(owner_key)

		validate_account_name(account_name)
		if account_exists(account_name):
			raise Exception(f"Account {account_name} already exists in the network")
		
		raw = get_account_creation_raw_params(account_name, active_key, owner_key)
		eosio_params = EosioParams(raw.params_actions_list, self.private_key)
		net_response = NodeNetwork.push_transaction(eosio_params.trx_json)
		if "transaction_id" not in net_response:
			raise Exception("Account creation trasaction was not successful")
		return net_response["transaction_id"]



	# TODO Patch eosiopy and raise error with message from JSON response in case of 
	# KeyError binargs
	def get_account_creation_raw_params(self, account_name, active_key, owner_key):
		return RawinputParams(
			"newaccount", {
				"creator":self.account,
				"newact":account_name,
				"owner":{
					"threshold":1,
					"keys":[{
						"key":owner_key,
						"weight":1
					}],
					"accounts":[],
					"waits":[]
				},
				"active":{
					"threshold":1,
					"keys":[{
						"key":active_key,
						"weight":1
					}],
					"accounts":[],
					"waits":[]
				}
			}, "eosio", self.permission
		).add (
			"buyrambytes", {
				"payer":self.account,
				"receiver":account_name,
				"bytes":"3000"
			}, "eosio", self.permission
		).add (
			"delegatebw", {
				"from":self.account,
				"receiver":account_name,
				"stake_net_quantity": "0.2000 EOS",
				"stake_cpu_quantity":"0.2000 EOS",
				"transfer":"0"
			}, "eosio", self.permission
		)


