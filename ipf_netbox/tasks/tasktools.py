from functools import wraps
from ipf_netbox.source import get_source


def with_sources(coro):
    @wraps(coro)
    async def wrapper(*vargs, **kwargs):
        nb_src = get_source("netbox")
        ipf_src = get_source("ipfabric")

        async with nb_src.client, ipf_src.client:
            ipf_src.client.api.timeout = 120
            nb_src.client.timeout = 120

            return await coro(ipf_src, nb_src, *vargs, **kwargs)

    return wrapper


def diff_report_brief(diff_res):
    print("\nDiff Report")
    print(f"   Missing: count {len(diff_res.missing)}")
    print(f"   Needs Update: count {len(diff_res.changes)}")
    print("\n")
