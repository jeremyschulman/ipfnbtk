import asyncio
from ipfnbtk.collections.devices import DeviceCollection
from ipfnbtk.sources.netbox import NetboxDeviceCollection
from itertools import chain

loop = asyncio.get_event_loop()
asyncio.set_event_loop(loop)

nb_dc = NetboxDeviceCollection()
# loop.run_until_complete(nb_dc.fetch())


async def run(page_sz):
    filters = {
        "exclude": "config_context",
        "platform__n": "null"
    }

    return await nb_dc.client.paginate(
        '/dcim/devices',
        page_sz=page_sz, filters=filters
    )


# nb_dc.client.timeout = 60
# devices = loop.run_until_complete(run(200))

loop.run_until_complete(nb_dc.fetch())
