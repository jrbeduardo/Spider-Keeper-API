from __future__ import unicode_literals

from requests import Session

from exceptions import SpiderKeeperResponseError

"""
El objeto Session, permite mantener ciertos parámetros a través 
de múltiples peticiones.
"""

class Client(Session):
    
    def _handle_response(self, response):
        """
        Maneja la respuesta recibida de SpiderKeeper..
        """
        result = response.json()
        return result

    def request(self, *args, **kwargs):
        response = super(Client, self).request(*args, **kwargs)
        return self._handle_response(response)