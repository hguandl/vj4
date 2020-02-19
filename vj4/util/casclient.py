import aiohttp
import json
import logging
from vj4 import error
from vj4.util import options

logger = logging.getLogger("cas")

async def __fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_user_info(ticket):
    response = await __fetch(
        f'https://cas.sustech.edu.cn/cas/p3/serviceValidate?service='
        f'{options.url_prefix}/auth/login&format=json&ticket={ticket}')
    try:
        udoc = json.loads(response)['serviceResponse']['authenticationSuccess']['attributes']
        logger.debug(udoc)
        return udoc
    except (TypeError, KeyError, ValueError):
        raise error.ValidationError('CAS ticket')
