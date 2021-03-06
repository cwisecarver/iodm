import asyncio
import logging

import tornado.web
import tornado.platform.asyncio

from iodm.server.api import v1
from iodm.server.api.base import Default404Handler


logger = logging.getLogger(__name__)


def make_app(debug=True):
    endpoints = [
        ('/v1/auth/?', v1.AuthHandler)
    ]

    for endpoint in reversed(v1.RESOURCES):
        endpoint = endpoint.as_handler_entry()
        endpoint = (
            '/{}{}'.format(v1.__name__.split('.')[-1], endpoint[0]),
            endpoint[1], endpoint[2]
        )
        endpoints.append(endpoint)
        logger.info('Loaded {} endpoint "{}"'.format(v1.__name__, endpoint[0]))

    return tornado.web.Application(
        endpoints,
        debug=debug,
        default_handler_class=Default404Handler,
    )


def profile(ktime=10):
    asyncio.get_event_loop().call_later(ktime, lambda: asyncio.get_event_loop().stop())
    main(debug=False)


def main(debug=True, host='127.0.0.1', port=1212):
    tornado.platform.asyncio.AsyncIOMainLoop().install()

    app = make_app(debug)

    app.listen(port, host)

    asyncio.get_event_loop().set_debug(debug)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()
