"""
TODO : more precise exception types
"""
from eosiopy import eosio_config
from .validation import validate_account_name, validate_private_key


def check_all_required_fields_are_provided(data):
    required_fields = ["network_type","api_gateway","api_port","account","private_key"]
    if False in [field in data for field in required_fields]:
        raise Exception("Some of required fields is missing")
    


TESTNET_NETWORK_ID = "5fff1dae8dc8e2fc4d5b23b2c7665c97f9e9d8edf2b6485a86ba311c25639191"
MAINNET_NETWORK_ID = "aca376f206b8fc25a6ed44dbdc66547c36c6c33e3a119ffbeaef943642f0e906"

"""
Be careful with adding inheritabce from object, .__dict__ of NetworkConfig instances
are used
"""
class NetworkConfig: 

    def set_network_type(self, network_type):
        if network_type in ["testnet", "mainnet"]:
            self.network_type = network_type
            if network_type == "mainnet":
                self.network_id = MAINNET_NETWORK_ID
            else:
                self.network_id = TESTNET_NETWORK_ID
        else:
            raise Exception("'network_type' parameter passed to Network must either be equal to \
                'testnet' or 'mainnet'")


    def set_api_gateway(self, api_gateway):
        self.api_gateway = api_gateway
        eosio_config.url = api_gateway


    def set_api_port(self, api_port):
        self.api_port = api_port
        eosio_config.port = api_port


    def set_account(self, account):
        validate_account_name(account)
        if not self.isset_api_params():
            raise Exception("You have to set EOSIO RPC API gateway and port first before setting \
                the account")

        from .utils import account_exists
        if account_exists(account):
            self.account = account
        else:
            raise Exception(f"Account {account} does not exist in {network_type}")
        self.permission = f"{account}@active"


    def set_private_key(self, private_key):
        validate_private_key(private_key)
        self.private_key = private_key


    def isset_api_params(self):
        return hasattr(self, 'api_gateway') and hasattr(self, 'api_port')


    def check_can_push_transactions(self):
        check_all_required_fields_are_provided(self.__dict__)


network_config = NetworkConfig()


def configure_network(data):
    check_all_required_fields_are_provided(data)
    network_config.set_network_type(data["network_type"])
    network_config.set_api_gateway(data["api_gateway"])
    network_config.set_api_port(data["api_port"])
    network_config.set_account(data["account"])
    network_config.set_private_key(data["private_key"])
