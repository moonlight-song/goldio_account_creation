from cherrypy import expose, request, dispatch, tools
from cherrypy import HTTPError

from .eos.main import Network # TODO add direct import of this one

@expose
class EOSAccountCreatorWebService(object):
	"""
	Service for EOS account creation
	"""
	@tools.json_in()
	@tools.json_out()
	def POST(self):
		"""
		Expected json : {
			"account_name" : str,
			"owner_key" : str,
			"active_key" : str #OPTIONAL,
			"tx_id" : str #TODO
		}
		Response codes :
		200 - OK
		415 - No JSON was passed
		400 - passed JSON misses some of required fields
		500 - smth happened on the server side, error message follows
		"""
		data = request.json

		self.check_required_fields(data)
		active_key = data['active_key'] if 'active_key' in data else None

		# Creating an account 
		# TODO improve exception handling
		try: 
			net = Network()
			success_tx_id = net.create_account(data['account_name'], data['owner_key'], active_key)
			return {'success_tx_id' : success_tx_id}

		except Exception as err:
			err_msg = ""
			for arg in err.args : err_msg += arg + " "
			raise HTTPError.handle(err, 500, err_msg)


	def check_required_fields(self, data):
		required_fields = ['account_name', 'owner_key']
		if False in [field in data for field in required_fields]:
			raise HTTPError(400, "Some of required fields is missing")


eos_account_creator_web_service_config = {
	'/': {
		'request.dispatch': dispatch.MethodDispatcher(),
	}
}