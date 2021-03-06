import json
import asyncio

import bcrypt

from iodm import NamespaceManager
from iodm.util import order_dictionary
from iodm.auth.providers.base import BaseAuthProvider

manager = NamespaceManager()


class SelfAuthProvider(BaseAuthProvider):
    name = 'self'
    type = 'tracked'

    USERNAME_SCHEMA = {
        'id': 'username',
        'type': 'string',
        'pattern': '^\w{1,64}$'
    }

    PASSWORD_SCHEMA = {
        'id': 'password',
        'type': 'string',
        'pattern': '^\$2b\$1[0-3]\$\S{53}$'
    }

    async def _authenticate(self, data):
        namespace = manager.get_namespace(data['namespace'])
        collection = namespace.get_collection(data['collection'])

        # TODO handle exceptions
        if not (
            collection.schema
            and 'username' in collection.schema._schema['required']
            and 'password' in collection.schema._schema['required']
            and collection.schema._schema['properties']['username'] == self.USERNAME_SCHEMA
            and collection.schema._schema['properties']['password'] == self.PASSWORD_SCHEMA
        ):
            raise Exception('BAD SCHEMA')

        # TODO validate retrieved document
        doc = collection.read(data['username'])
        password = doc.data['password'].encode()

        hashed = await asyncio.get_event_loop().run_in_executor(None, lambda: bcrypt.hashpw(data['password'].encode(), password))

        if hashed == password:
            return 'tracked', '{}|{}'.format(namespace.name, data['collection']), data['username']
        raise Exception('BAD PASSWORD')
