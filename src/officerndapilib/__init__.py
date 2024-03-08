import requests
from datetime import datetime, timedelta

from officerndapilib.schema import (
    ORNDAuth,
    ORNDMember,
    ORNDResource,
    ORNDResourceType,
    ORNDBookingDateTime,
    ORNDBooking,
)

from officerndapilib.queries import (
    ORNDResourceQuery,
    append_queries_to_url,
)

from .exceptions import HttpException


ORND_BASE_URL = "https://app.officernd.com/api/v1/organizations/"

# AUTH


def get_ornd_token(auth: ORNDAuth) -> str:
    url = "https://identity.officernd.com/oauth/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
    }
    body = {
        "client_id": auth["client_id"],
        "client_secret": auth["client_secret"],
        "grant_type": auth["grant_type"],
        "scope": auth["scope"],
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
    token: str,
    organization: str,
    office: str,
    type: ORNDResourceType,
    queries: list[ORNDResourceQuery] = [],
) -> list[ORNDResource]:
    """Retrieves resources for a given office location from OfficeRND API"""

    url = ORND_BASE_URL + organization + f"/resources"
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


def get_resource_by_id(organization: str, id: str) -> ORNDResource:
    """Retrieves a specific resource by ID from OfficeRND API"""

    url = ORND_BASE_URL + organization + f"/resources/{id}"
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
    RetrieveORNDBookingOccurencesRequest,
)

# MEMBERS


def get_all_members(
    token: str, organization: str, office: str
) -> list[ORNDMember]:
    """Retrieves all members from OfficeRND API"""

    url = ORND_BASE_URL + organization + f"/members?office={office}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        data: list[ORNDMember] = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def get_member_by_id(token: str, organization: str, id: str) -> ORNDMember:
    """Retrieves a specific member by ID from OfficeRND API"""

    url = ORND_BASE_URL + organization + f"/members/{id}"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.ok:
        data: ORNDMember = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def get_member_by_email(
    token: str, organization: str, office: str, email: str
) -> ORNDMember:
    """Retrieves a specific member by email from OfficeRND API"""

    url = ORND_BASE_URL + organization + f"/members?office={office}"
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
            raise StopIteration(f"Member with email '{email}' not found")
    else:
        raise Exception(response.json()["message"])


def create_member(
    token: str, organization: str, member_request: CreateORNDMemberRequest
) -> list[ORNDMember]:
    """Creates a member in OfficeRND"""

    url = ORND_BASE_URL + organization + f"/members"
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


def delete_members(
    token: str, organization: str, ids: list[str]
) -> list[ORNDMember]:
    """Deletes a member in OfficeRND"""

    url = ORND_BASE_URL + organization + f"/members"
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


def get_all_bookings(
    token: str,
    organization: str,
    booking_occurence: RetrieveORNDBookingOccurencesRequest,
) -> list[ORNDBooking]:
    """Retrieves all bookings from OfficeRND API"""

    url = ORND_BASE_URL + organization + f"/bookings/occurrences?"
    url += f"$limit={booking_occurence.limit}&start={booking_occurence.start}&end={booking_occurence.end}\
        &resourceId={booking_occurence.resource_id}&office={booking_occurence.office}"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        data: list[ORNDBooking] = response.json()
        return data
    else:
        raise Exception(response.json()["message"])


def get_booking_times_available_on_date(
    booking_times: list[dict[str, ORNDBookingDateTime]],
    date: str,
    start=9,
    end=17,
    interval=60,
) -> list[str]:
    """Returns a list of times available for booking on a given date"""

    # array of times from start to end in min intervals
    times = [
        f"{hour:02d}:{min:02d}"
        for hour in range(start, end)
        for min in range(0, 60, interval)
    ]

    # filter the times to only include times that are on the date
    booking_times = [
        booking_time
        for booking_time in booking_times
        if booking_time["start"]["dateTime"].split("T")[0] == date
    ]

    # filter the times that are already booked between the start[dateTime] and end[dateTime]
    booked_intervals = []
    for booking in booking_times:
        # round down to the nearest min interval
        start_dt = datetime.fromisoformat(booking["start"]["dateTime"])
        if start_dt.minute % interval != 0:
            start_dt = start_dt - timedelta(minutes=start_dt.minute % interval)

        # round up to the nearest min interval
        end_dt = datetime.fromisoformat(booking["end"]["dateTime"])
        if end_dt.minute % interval != 0:
            end_dt = end_dt + timedelta(
                minutes=interval - end_dt.minute % interval
            )

        duration_min_intervals = (end_dt - start_dt).seconds / 1800

        booked_intervals.append(start_dt.strftime("%H:%M"))
        for _ in range(int(duration_min_intervals) - 1):
            start_dt += timedelta(minutes=interval)
            booked_intervals.append(start_dt.strftime("%H:%M"))

        print(booked_intervals)

    # remove booked intervals from available times
    times = [time for time in times if time not in booked_intervals]

    # return list of hours that are available
    return times


def validate_booking_request(
    token: str,
    organization: str,
    booking_request: CreateORNDMemberBookingRequest,
) -> list[ORNDBooking]:
    """Validates a booking request"""

    url = ORND_BASE_URL + organization + f"/bookings/checkout-summary"
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
        raise Exception(response.json()["message"])


def create_booking(
    token: str,
    organization: str,
    booking_request: CreateORNDMemberBookingRequest,
) -> list[ORNDBooking]:
    """Creates a booking in OfficeRND"""

    url = ORND_BASE_URL + organization + f"/bookings/checkout"
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
    token: str,
    organization: str,
    booking_request: CreateORNDMemberBookingRequest,
) -> list[ORNDBooking]:
    """Validates a booking request made has been created in OfficeRND"""

    url = ORND_BASE_URL + organization + f"/bookings/summary"
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


def booking_checkout(
    token: str,
    organization: str,
    booking_request: CreateORNDMemberBookingRequest,
):
    """Validates and creates a booking in OfficeRND"""
    validate_booking_request(token, organization, booking_request)
    validate_booking_creation(token, organization, booking_request)
    booking = create_booking(token, organization, booking_request)
    return booking
