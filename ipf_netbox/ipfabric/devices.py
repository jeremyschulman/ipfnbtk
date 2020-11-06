# -----------------------------------------------------------------------------
# System Imports
# -----------------------------------------------------------------------------

from typing import Dict, Tuple, Any

from aioipfabric.filters import parse_filter

# -----------------------------------------------------------------------------
# Private Imports
# -----------------------------------------------------------------------------

from ipf_netbox.collection import Collection
from ipf_netbox.collections.devices import DeviceCollection
from ipf_netbox.ipfabric.source import IPFabricSource
from ipf_netbox.mappings import normalize_hostname

# -----------------------------------------------------------------------------
# Exports
# -----------------------------------------------------------------------------

__all__ = ["IPFabricDeviceCollection"]


# -----------------------------------------------------------------------------
#
#                              CODE BEGINS
#
# -----------------------------------------------------------------------------


class IPFabricDeviceCollection(Collection, DeviceCollection):
    source_class = IPFabricSource

    async def fetch(self, **params):
        if (filters := params.get("filters")) is not None:
            params["filters"] = parse_filter(filters)

        self.inventory.extend(await self.source.client.fetch_devices(**params))

    def fingerprint(self, rec: Dict) -> Tuple[Any, Dict]:
        return (
            None,
            dict(
                sn=rec["sn"],
                hostname=normalize_hostname(rec["hostname"]),
                ipaddr=rec["loginIp"],
                site=rec["siteName"],
                os_name=rec["family"],
                vendor=rec["vendor"],
                model=rec["model"],
            ),
        )
