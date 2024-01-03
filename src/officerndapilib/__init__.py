import os
import requests
from datetime import datetime
from typing import Optional
from pprint import pprint

from .schema import (
    ORNDUser,
    ORNDUserAuthToken,
    ORNDMember,
    ORNDMemberBookingRequest,
    ORNDAddMemberRequest,
    ORNDResource,
    ORNDBookingRequest,
    ORNDBooking,
    ORNDResourceRate,
    ORNDResourceType,
    ORNDAddress,
)

from .queries import (
    ORNDBaseQuery,
    ORNDResourceQuery,
    ORNDMemberQuery,
    ORNDCompanyQuery,
    append_queries_to_url,
)

from .exceptions import HttpException

ORND_BASE_URL = "https://app.officernd.com/api/v1/organizations/"
ORND_ORG_SLUG = "re-defined"


def get_ornd_token() -> str:
    url = "https://identity.officernd.com/oauth/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
    }
    body = {
        "client_id": os.getenv("ORND_CLIENT_ID"),
        "client_secret": os.getenv("ORND_CLIENT_SECRET"),
        "grant_type": os.getenv("ORND_GRANT_TYPE"),
        "scope": os.getenv("ORND_SCOPE"),
    }
    response = requests.post(url, headers=headers, data=body)
    if response.ok:
        data: dict[str, str] = response.json()
        access_token = data["access_token"]
        return access_token
    else:
        raise Exception("Unable to authorize request")


# RESOURCES


def get_all_resources(
    office_id: str,
    type: ORNDResourceType,
    queries: list[ORNDResourceQuery] = [],
) -> list[ORNDResource]:
    """Retrieves resources for a given office location from OfficeRND API"""

    token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/resources"
    url = append_queries_to_url(url, queries)
    url += f"&office={office_id}&type={type}"

    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)

    if response.ok:
        data: list[ORNDResource] = response.json()
        return data
    else:
        err = response.json()["message"]
        print(err)
        raise HttpException(err, response.status_code)


def get_resource_by_id(id: str) -> ORNDResource:
    """Retrieves a specific resource by ID from OfficeRND API"""

    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/resources/{id}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.ok:
        data: ORNDResource = response.json()
        return data
    else:
        raise Exception(response.json()["message"])
