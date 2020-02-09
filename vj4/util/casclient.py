import aiohttp
import json
from vj4 import error
from vj4.util import options


async def __fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


async def get_user_info(ticket):
    response = await __fetch(
        f'https://cas.sustc.edu.cn/cas/p3/serviceValidate?service='
        f'{options.url_prefix}/auth/login&format=json&ticket={ticket}')
    try:
        return json.loads(response)['serviceResponse']['authenticationSuccess']['attributes']
    except (TypeError, KeyError, ValueError):
        raise error.ValidationError('CAS ticket')
