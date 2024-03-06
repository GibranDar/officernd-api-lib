from typing import cast

import requests

from officerndapilib.schema import (
    ORNDMember,
    ORNDResource,
    ORNDResourceType,
    ORNDBooking,
)

from officerndapilib.queries import (
    ORNDResourceQuery,
    append_queries_to_url,
)

from .exceptions import HttpException

# ENV

import dotenv
from dotenv import load_dotenv

load_dotenv()

ORND_BASE_URL = "https://app.officernd.com/api/v1/organizations/"
ORND_ORG_SLUG = cast(str, dotenv.get_key(dotenv.find_dotenv(), "ORND_ORG_SLUG"))

# AUTH


def get_ornd_token() -> str:
    url = "https://identity.officernd.com/oauth/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
    }
    body = {
        "client_id": dotenv.get_key(dotenv.find_dotenv(), "ORND_CLIENT_ID"),
        "client_secret": dotenv.get_key(
            dotenv.find_dotenv(), "ORND_CLIENT_SECRET"
        ),
        "grant_type": dotenv.get_key(dotenv.find_dotenv(), "ORND_GRANT_TYPE"),
        "scope": dotenv.get_key(dotenv.find_dotenv(), "ORND_SCOPE"),
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


from officerndapilib.reqs import (
    CreateORNDMemberRequest,
    CreateORNDMemberBookingRequest,
)

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

    token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/members/{id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
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


def validate_booking_request(
    booking_request: CreateORNDMemberBookingRequest,
    token: str = "",
) -> list[ORNDBooking]:
    """Validates a booking request"""

    if not token:
        token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/bookings/checkout-summary"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    response = requests.post(url, headers=headers, json=booking_request.data)
    if response.ok:
        data: list[ORNDBooking] = response.json()
        return data
    else:
        print(response.json())
        raise Exception(response.json()["message"])


def create_booking(
    booking_request: CreateORNDMemberBookingRequest,
    token: str = "",
) -> list[ORNDBooking]:
    """Creates a booking in OfficeRND"""

    if not token:
        token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/bookings/checkout"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    payload = booking_request.data

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        data: list[ORNDBooking] = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def validate_booking_creation(
    booking_request: CreateORNDMemberBookingRequest, token: str = ""
) -> list[ORNDBooking]:
    """Validates a booking request made has been created in OfficeRND"""

    if not token:
        token = get_ornd_token()
    url = ORND_BASE_URL + ORND_ORG_SLUG + f"/bookings/summary"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    booking_obj = {
        "resourceId": booking_request.resourceId,
        "start": {"dateTime": booking_request.start},
        "end": {"dateTime": booking_request.end},
    }
    booking_target = {"member": booking_request.member}
    payload = {
        "booking": booking_obj,
        "target": booking_target,
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.ok:
        data: list[ORNDBooking] = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def booking_checkout(booking_request: CreateORNDMemberBookingRequest):
    """Validates and creates a booking in OfficeRND"""

    token = get_ornd_token()
    validate_booking_request(booking_request, token)
    validate_booking_creation(booking_request, token)
    booking = create_booking(booking_request, token)
    return booking
