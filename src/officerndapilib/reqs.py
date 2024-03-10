import re
from datetime import datetime, timezone
from typing import Optional

from attrs import define, field, validators, converters, asdict

from officerndapilib import get_resource_by_id
from officerndapilib.exceptions import ValidationException


def attrs_is_email(instance, attribute, value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValueError(f"{value} is not a valid email address")


def attrs_valid_ornd_id(instance, attribute, value):
    if not re.match(r"^[0-9a-fA-F]{24}$", value):
        raise ValueError(f"{value} is not a valid ORND ID")


def attrs_valid_ornd_password(instance, attribute, value):
    """
    Password must be at least 8 characters long and contain 3 out of the 4 elements:
    uppercase letter, lowercase letter, digit or symbol.
    """
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d|\W).{8,}$", value):
        raise ValueError(f"{value} is not a valid password")


def attrs_is_ISO8601_datetime(instance, attribute, value):
    dt_obj = datetime.fromisoformat(value)  # raises ValueError if not valid
    dt_str = value.split("T")
    if len(dt_str) != 2:
        raise ValueError(f"{value} is not a valid datetime")
    date, time = dt_str
    if not re.match(r"\d{4}-\d{2}-\d{2}", date):
        raise ValueError(f"{date} is not a valid date")
    if not re.match(r"\d{2}:\d{2}(:\d{2})?(Z)?", time):
        raise ValueError(f"{time} is not a valid time")


def attrs_is_ISO8601_date(instance, attribute, value):
    if not re.match(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"{value} is not a valid date")


@define(kw_only=True)
class CreateORNDMemberRequest:
    startDate: str = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_datetime]
    )
    office: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )
    name: str = field(validator=[validators.instance_of(str)])
    email: str = field(validator=[validators.instance_of(str), attrs_is_email])
    phone: Optional[str] = field(
        default=None,
        converter=converters.optional(str),
        validator=[validators.optional(validators.instance_of(str))],
    )
    description: Optional[str] = field(
        default=None,
        validator=[validators.optional(validators.instance_of(str))],
    )
    properties: Optional[dict[str, str]] = field(
        default=None,
        validator=[validators.optional(validators.instance_of(dict))],
    )
    address: Optional[dict[str, str]] = field(
        default=None,
        validator=[validators.optional(validators.instance_of(dict))],
    )

    @property
    def data(self):
        return asdict(self)


@define(kw_only=True)
class CreateORNDTeamMemberRequest(CreateORNDMemberRequest):
    team: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )


@define(kw_only=True, frozen=True)
class CreateORNDWebBookingRequest:
    organization: str = field(validator=[validators.instance_of(str)])
    office: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )
    resource_id: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )
    start: str = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_datetime]
    )
    end: str = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_datetime]
    )
    summary: str = field(
        validator=[validators.instance_of(str)]
    )  # Booking Title
    description: Optional[str] = field(
        default=None,
        validator=[validators.optional(validators.instance_of(str))],
    )  # Booking Description
    count: int = field(default=1, validator=[validators.instance_of(int)])
    source: str = field(
        default="website", validator=[validators.instance_of(str)]
    )
    free: bool = field(
        default=False,
        validator=[validators.instance_of(bool)],
    )

    @property
    def data(self):
        return asdict(self)

    def __attrs_post_init__(self):
        self.run_validations()

    def is_bookable_resource(self) -> bool:
        resource = get_resource_by_id(self.organization, self.resource_id)
        if resource["type"] not in [
            "meeting_room",
            "hotdesk",
        ]:
            raise ValidationException(
                f"{resource['name']} is not a bookable resource"
            )
        return False

    def is_start_before_end(self) -> bool:
        start = datetime.fromisoformat(self.start)
        end = datetime.fromisoformat(self.end)
        if start > end:
            raise ValidationException("Booking start is after end")
        return True

    def is_weekday(self) -> bool:
        start = datetime.fromisoformat(self.start)
        end = datetime.fromisoformat(self.end)
        if start.weekday() in [5, 6] or end.weekday() in [5, 6]:
            raise ValidationException("Booking is on a weekend")
        return True

    def is_not_outside_office_hours(self) -> bool:
        start = datetime.fromisoformat(self.start)
        end = datetime.fromisoformat(self.end)
        if (
            start.time() < datetime.strptime("09:00", "%H:%M").time()
            or end.time() > datetime.strptime("18:00", "%H:%M").time()
        ):
            raise ValidationException("Booking is outside office hours")
        return True

    def is_not_longer_than_8_hours(self) -> bool:
        start = datetime.fromisoformat(self.start)
        end = datetime.fromisoformat(self.end)
        if (end - start).seconds / 3600 > 8:
            raise ValidationException("Booking is longer than 8 hours")
        return True

    def is_not_in_the_past(self) -> bool:
        start = datetime.fromisoformat(self.start)
        start = start.replace(tzinfo=timezone.utc)
        if start < datetime.now(timezone.utc):
            raise ValidationException("Booking is in the past")
        return True

    def is_not_greater_than_30_days_in_future(self) -> bool:
        now = datetime.now(timezone.utc)
        booking_start = datetime.fromisoformat(self.start)
        booking_start = booking_start.replace(tzinfo=timezone.utc)
        if (booking_start - now).days > 30:
            raise ValidationException("Booking is greater than 30 days")
        return True

    def run_validations(self):
        self.is_bookable_resource()
        self.is_start_before_end()
        self.is_weekday()
        self.is_not_in_the_past()
        self.is_not_outside_office_hours()
        self.is_not_longer_than_8_hours()
        self.is_not_greater_than_30_days_in_future()


@define(kw_only=True)
class CreateORNDMemberBookingRequest(CreateORNDWebBookingRequest):
    member: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )


@define(kw_only=True)
class CreateORNDTeamBookingRequest(CreateORNDWebBookingRequest):
    team: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )


@define(kw_only=True)
class RetrieveORNDBookingOccurencesRequest:
    office: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )
    resource_id: str = field(
        validator=[validators.instance_of(str), attrs_valid_ornd_id]
    )
    start: Optional[str] = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_date]
    )
    end: Optional[str] = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_date]
    )
    limit: int = field(default=100, validator=[validators.instance_of(int)])

    @property
    def data(self):
        return asdict(self)
