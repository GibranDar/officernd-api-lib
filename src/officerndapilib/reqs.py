import re
from datetime import datetime
from typing import Optional

from attrs import define, field, validators, converters, asdict


def attrs_is_email(instance, attribute, value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValueError(f"{value} is not a valid email address")


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


@define(kw_only=True)
class CreateORNDMemberRequest:
    startDate: str = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_datetime]
    )
    office: str = field(validator=[validators.instance_of(str)])
    name: str = field(validator=[validators.instance_of(str)])
    email: str = field(validator=[validators.instance_of(str), attrs_is_email])
    phone: Optional[str] = field(
        default=None,
        converter=converters.optional(str),
        validator=[validators.optional(validators.instance_of(str))],
    )
    description: Optional[str] = field(
        validator=[validators.optional(validators.instance_of(str))]
    )
    properties: Optional[dict[str, str]] = field(
        validator=[validators.optional(validators.instance_of(dict))]
    )
    address: Optional[dict[str, str]] = field(
        validator=[validators.optional(validators.instance_of(dict))]
    )

    @property
    def data(self):
        return asdict(self)


@define(kw_only=True)
class CreateORNDTeamMemberRequest(CreateORNDMemberRequest):
    team: str = field(validator=[validators.instance_of(str)])


@define(kw_only=True)
class CreateORNDWebBookingRequest:
    office: str = field(validator=[validators.instance_of(str)])
    resourceId: str = field(validator=[validators.instance_of(str)])
    start: str = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_datetime]
    )
    end: str = field(
        validator=[validators.instance_of(str), attrs_is_ISO8601_datetime]
    )
    source: str = field(
        default="website", validator=[validators.instance_of(str)]
    )
    summary: str = field(
        validator=[validators.instance_of(str)]
    )  # Booking Title
    description: Optional[str] = field(
        validator=[validators.optional(validators.instance_of(str))]
    )  # Booking Description
    free: bool = field(
        default=False,
        validator=[validators.instance_of(bool)],
    )

    @property
    def data(self):
        return asdict(self)


@define(kw_only=True)
class CreateORNDMemberBookingRequest(CreateORNDWebBookingRequest):
    member: str = field(validator=[validators.instance_of(str)])


@define(kw_only=True)
class CreateORNDTeamBookingRequest(CreateORNDWebBookingRequest):
    team: str = field(validator=[validators.instance_of(str)])
