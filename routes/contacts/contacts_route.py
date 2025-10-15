from flask_restful import Api
from controllers.contacts.list_my_contacts_controller import ListMyContactsControler
from controllers.contacts.create_new_contact_controller import CreateNewContactController

def register_contacts_route(api: Api):
    api.add_resource(CreateNewContactController, '/contacts', methods=['POST'], endpoint='create_contact')
    api.add_resource(ListMyContactsControler, '/contacts', methods=['GET'], endpoint='list_contacts')