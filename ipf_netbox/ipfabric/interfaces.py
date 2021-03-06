from typing import Dict

from aioipfabric.filters import parse_filter

from ipf_netbox.collection import Collector
from ipf_netbox.collections.interfaces import InterfaceCollection
from ipf_netbox.ipfabric.source import IPFabricSource

from ipf_netbox.mappings import expand_interface, normalize_hostname


class IPFabricInterfaceCollection(Collector, InterfaceCollection):
    source_class = IPFabricSource

    async def fetch(self, **params):

        if (filters := params.get("filters")) is not None:
            params["filters"] = parse_filter(filters)

        self.source_records.extend(
            await self.source.client.fetch_table(
                url="/tables/inventory/interfaces",
                columns=["hostname", "intName", "dscr", "siteName"],
                **params,
            )
        )

    def fingerprint(self, rec: Dict) -> Dict:
        return {
            "interface": expand_interface(rec["intName"]),
            "hostname": normalize_hostname(rec["hostname"]),
            "description": rec["dscr"] or "",
            "site": rec["siteName"],
        }
