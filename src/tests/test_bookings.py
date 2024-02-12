import pytest
import os
from datetime import datetime, timedelta, timezone
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from officerndapilib import (
    validate_booking_request,
    create_booking,
    validate_booking_creation,
)
from officerndapilib.reqs import CreateORNDMemberBookingRequest

WW_12MOORGATE = "65416bf72db05a7176b467ac"
WW_12M_MEETING_ROOM = "65c38ead5e6d7bd36ed6a540"  # LGC

TEST_BOOKING_START_DATE = (
    datetime.now(timezone.utc) + timedelta(days=1)
).replace(hour=9, minute=0, second=0)
TEST_BOOKING_SUMMARY = "Test Booking 1"
TEST_BOOKING_DESCRIPTION = "Test Booking 1 Description"

TEST_MEMBER = "65caaa8d836bde4655bca4de"

BOOKING_REQUEST = CreateORNDMemberBookingRequest(
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


def test_validate_booking_request():
    booking = validate_booking_request(BOOKING_REQUEST)
    pprint(booking, sort_dicts=False, indent=2, width=120)
    assert len(booking) > 0


def test_validate_booking_creation():
    booking = validate_booking_creation(BOOKING_REQUEST)
    assert len(booking) > 0


def test_create_booking():
    booking = create_booking(BOOKING_REQUEST)
    pprint(booking, sort_dicts=False, indent=2, width=120)
    assert len(booking) > 0
