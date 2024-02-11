import pytest
import os
from datetime import datetime, timedelta, timezone
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from officerndapilib import validate_booking_request
from officerndapilib.reqs import CreateORNDMemberBookingRequest

WW_12MOORGATE = "65416bf72db05a7176b467ac"
WW_12M_MEETING_ROOM = "65522d3a3e6de97c56019b32"  # LGC

TEST_BOOKING_START_DATE = (
    datetime.now(timezone.utc) + timedelta(days=1)
).replace(hour=9, minute=0, second=0)
TEST_BOOKING_SUMMARY = "Test Booking 1"
TEST_BOOKING_DESCRIPTION = "Test Booking 1 Description"

GD_MEMBER = "64ff1311a53ef27acade85bb"


def test_validate_booking_request():
    booking_request = CreateORNDMemberBookingRequest(
        office=WW_12MOORGATE,
        resourceId=WW_12M_MEETING_ROOM,
        start=TEST_BOOKING_START_DATE.isoformat(),
        end=(TEST_BOOKING_START_DATE + timedelta(hours=1)).isoformat(),
        count=1,
        source="website",
        summary=TEST_BOOKING_SUMMARY,
        description=TEST_BOOKING_DESCRIPTION,
        free=False,
        member=GD_MEMBER,
    )
    booking = validate_booking_request(booking_request)
    pprint(booking, sort_dicts=False, indent=2, width=120)
    assert booking
