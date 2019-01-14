from requests import post
from .config import network_config


def test_connection():
	url = f"{network_config.api_gateway}:{network_config.api_port}/v1/chain/get_info"
	result = post(url)
	if "chain_id" in result.json(): 
		if result.json()["chain_id"] != network_config.network_id:
			raise ConnectionError(f"CHAIN ID does not match, attempted to connect to \
				{network_config.network_type}")
	else:
		raise ConnectionError(f"{network_config.api_gateway}:{network_config.api_port} does not appear to be \
			{network_config.network_type} RPC API endpoint")


def account_exists(account_name):
	url = f"{network_config.api_gateway}:{network_config.api_port}/v1/chain/get_account"
	result = post(url, json={'account_name' : account_name})
	return result.status_code == 200 and result.json()['account_name'] == account_name 