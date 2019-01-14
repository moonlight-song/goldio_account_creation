import cherrypy
from service.eos.config import configure_network
from config import cherrypy_global_config, eos_config

from service.account_creation_app import EOSAccountCreatorWebService, eos_account_creator_web_service_config


def main():
	cherrypy.config.update(cherrypy_global_config)
	configure_network(eos_config)
	
	cherrypy.tree.mount(EOSAccountCreatorWebService(), '/api/create_account', 
		eos_account_creator_web_service_config)
	
	cherrypy.engine.start()
	cherrypy.engine.block()


if __name__ == '__main__':
	main()
