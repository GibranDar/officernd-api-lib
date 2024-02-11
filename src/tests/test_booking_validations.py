import pytest
import os
from datetime import datetime, timedelta, timezone
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from officerndapilib.reqs import CreateORNDMemberBookingRequest

WW_12MOORGATE = "65416bf72db05a7176b467ac"
WW_12M_MEETING_ROOM = "65522d3a3e6de97c56019b32"  # LGC
WW_12M_TEAM_ROOM = "65522f231e1a952e6a8f3655"  # 1F

GD_MEMBER = "64ff1311a53ef27acade85bb"

TEST_BOOKING_PARTIAL = {
    "office": WW_12MOORGATE,
    "count": 1,
    "source": "website",
    "summary": "Test Booking 1",
    "description": "Test Booking 1 Description",
    "free": False,
    "member": GD_MEMBER,
}

TEST_BOOKING_START_DATE = (
    datetime.now(timezone.utc) + timedelta(days=1)
).replace(hour=9, minute=0, second=0)


def test_validates_booking_request():
    booking_request = CreateORNDMemberBookingRequest(
        resourceId=WW_12M_MEETING_ROOM,
        start=TEST_BOOKING_START_DATE.isoformat(),
        end=(TEST_BOOKING_START_DATE + timedelta(hours=1)).isoformat(),
        **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
    )
    assert booking_request.data


def test_booking_is_bookable_resource():
    with pytest.raises(ValueError):
        booking_request = CreateORNDMemberBookingRequest(
            resourceId=WW_12M_TEAM_ROOM,
            start=TEST_BOOKING_START_DATE.isoformat(),
            end=(TEST_BOOKING_START_DATE + timedelta(hours=1)).isoformat(),
            **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
        )


def test_booking_start_is_before_end():
    with pytest.raises(ValueError):
        booking_request = CreateORNDMemberBookingRequest(
            resourceId=WW_12M_MEETING_ROOM,
            start=TEST_BOOKING_START_DATE.replace(hour=11).isoformat(),
            end=(TEST_BOOKING_START_DATE + timedelta(hours=-1)).isoformat(),
            **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
        )


def test_booking_is_before_office_hours():
    with pytest.raises(ValueError):
        end = TEST_BOOKING_START_DATE + timedelta(hours=1)
        booking_request = CreateORNDMemberBookingRequest(
            resourceId=WW_12M_MEETING_ROOM,
            start=TEST_BOOKING_START_DATE.replace(
                hour=8, minute=0, second=0
            ).isoformat(),
            end=end.isoformat(),
            **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
        )


def test_booking_is_after_office_hours():
    with pytest.raises(ValueError):
        booking_request = CreateORNDMemberBookingRequest(
            resourceId=WW_12M_MEETING_ROOM,
            start=TEST_BOOKING_START_DATE.isoformat(),
            end=TEST_BOOKING_START_DATE.replace(
                hour=19, minute=0, second=0
            ).isoformat(),
            **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
        )


def test_booking_is_longer_than_8_hours():
    with pytest.raises(ValueError):
        booking_request = CreateORNDMemberBookingRequest(
            resourceId=WW_12M_MEETING_ROOM,
            start=TEST_BOOKING_START_DATE.isoformat(),
            end=(TEST_BOOKING_START_DATE + timedelta(hours=9)).isoformat(),
            **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
        )


def test_booking_is_in_the_past():
    with pytest.raises(ValueError):
        past_date = TEST_BOOKING_START_DATE + timedelta(days=-1)
        booking_request = CreateORNDMemberBookingRequest(
            resourceId=WW_12M_MEETING_ROOM,
            start=past_date.isoformat(),
            end=(past_date + timedelta(hours=8)).isoformat(),
            **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
        )


def test_booking_is_greater_than_30_days_in_future():
    with pytest.raises(ValueError):
        future_date = TEST_BOOKING_START_DATE + timedelta(days=31)
        booking_request = CreateORNDMemberBookingRequest(
            resourceId=WW_12M_MEETING_ROOM,
            start=TEST_BOOKING_START_DATE.isoformat(),
            end=(future_date + timedelta(hours=8)).isoformat(),
            **TEST_BOOKING_PARTIAL,  # type:ignore[arg-type]
        )
