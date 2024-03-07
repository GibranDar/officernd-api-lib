import pytest
import os
from datetime import datetime, timedelta, timezone
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from officerndapilib import (
    get_ornd_token,
    validate_booking_request,
    create_booking,
    validate_booking_creation,
)
from officerndapilib.schema import ORNDAuth
from officerndapilib.reqs import CreateORNDMemberBookingRequest

ORND_AUTH = ORNDAuth(
    client_id=os.getenv("ORND_CLIENT_ID", ""),
    client_secret=os.getenv("ORND_CLIENT_SECRET", ""),
    grant_type=os.getenv("ORND_GRANT_TYPE", ""),
    scope=os.getenv("ORND_SCOPE", ""),
    organization_slug="re-defined-test-account",
)

ORND_ORGANIZATION = os.getenv("ORND_ORG_SLUG", "")

WW_12MOORGATE = "65416bf72db05a7176b467ac"
WW_12M_MEETING_ROOM = "65c38ead5e6d7bd36ed6a540"  # LGC

TEST_BOOKING_START_DATE = (
    datetime.now(timezone.utc) + timedelta(days=1)
).replace(hour=9, minute=0, second=0)
TEST_BOOKING_SUMMARY = "Test Booking 1"
TEST_BOOKING_DESCRIPTION = "Test Booking 1 Description"

TEST_MEMBER = "65caaa8d836bde4655bca4de"

BOOKING_REQUEST = CreateORNDMemberBookingRequest(
    organization=ORND_ORGANIZATION,
    office=WW_12MOORGATE,
    resourceId=WW_12M_MEETING_ROOM,
    start=TEST_BOOKING_START_DATE.isoformat(),
    end=(TEST_BOOKING_START_DATE + timedelta(hours=1)).isoformat(),
    count=1,
    source="website",
    summary=TEST_BOOKING_SUMMARY,
    description=TEST_BOOKING_DESCRIPTION,
    free=False,
    member=TEST_MEMBER,
)


@pytest.fixture
def token():
    return get_ornd_token(ORND_AUTH)


def test_validate_booking_request(token):
    booking = validate_booking_request(
        token, ORND_ORGANIZATION, BOOKING_REQUEST
    )
    pprint(booking, sort_dicts=False, indent=2, width=120)
    assert len(booking) > 0


def test_validate_booking_creation(token):
    booking = validate_booking_creation(
        token, ORND_ORGANIZATION, BOOKING_REQUEST
    )
    assert len(booking) > 0


def test_create_booking(token):
    booking = create_booking(token, ORND_ORGANIZATION, BOOKING_REQUEST)
    pprint(booking, sort_dicts=False, indent=2, width=120)
    assert len(booking) > 0
