import os
import requests

from officerndapilib.schema import (
    ORNDMember,
    ORNDResource,
    ORNDResourceType,
)

from officerndapilib.queries import (
    ORNDResourceQuery,
    append_queries_to_url,
)

from officerndapilib.reqs import (
    CreateORNDMemberRequest,
)

from .exceptions import HttpException

ORND_BASE_URL = "https://app.officernd.com/api/v1/organizations/"
ORND_ORG_SLUG = "re-defined"


# AUTH


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
    office: str,
    type: ORNDResourceType,
    queries: list[ORNDResourceQuery] = [],
) -> list[ORNDResource]:
    """Retrieves resources for a given office location from OfficeRND API"""

    token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/resources"
    url = append_queries_to_url(url, queries)
    url += f"&office={office}&type={type}"

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


# MEMBERS


def get_all_members(office: str) -> list[ORNDMember]:
    """Retrieves all members from OfficeRND API"""

    token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/members?office={office}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        data: list[ORNDMember] = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def get_member_by_id(id: str) -> ORNDMember:
    """Retrieves a specific member by ID from OfficeRND API"""

    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/members/{id}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.ok:
        data: ORNDMember = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def get_member_by_email(office: str, email: str) -> ORNDMember:
    """Retrieves a specific member by email from OfficeRND API"""

    token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/members?office={office}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        data: list[ORNDMember] = response.json()

        try:
            member: ORNDMember = next(
                member for member in data if member["email"] == email
            )
            return member
        except StopIteration:
            raise Exception(f"Member with email '{email}' not found")
    else:
        raise Exception(response.json()["message"])


def create_member(member_request: CreateORNDMemberRequest) -> list[ORNDMember]:
    """Creates a member in OfficeRND"""

    token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/members"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = member_request.data

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        data: list[ORNDMember] = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def delete_members(ids: list[str]) -> list[ORNDMember]:
    """Deletes a member in OfficeRND"""

    token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/members"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.delete(url, headers=headers, json=ids)
    if response.ok:
        data: list[ORNDMember] = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


# BOOKINGS


def validate_booking_request(booking_request: CreateORNDMemberRequest):
    """Validates a booking request"""
    pass
