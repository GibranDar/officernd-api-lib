from datetime import datetime
from typing import TypedDict, Literal, Optional, Union, Any


ORNDResourceType = Literal[
    "meeting_room", "team_room", "desk_tr", "desk", "hotdesk", "hd_daily"
]
ORNDMemberStatus = Literal["active", "contact", "former"]
ORNDUserAuthToken = TypedDict("ORNDUserAuthToken", {"token": str})


class ORNDAuth(TypedDict):
    client_id: str
    client_secret: str
    grant_type: str
    scope: str
    organization_slug: str


class ORNDResourceAccess(TypedDict):
    full: bool
    public: bool
    teams: list[str]
    plans: list[str]


class ORNDResourceAvailability(TypedDict):
    startDate: str
    endDate: Optional[str]


class ORNDResourceRate(TypedDict):
    useValueCredits: bool
    type: str
    intervalLength: str
    intervalCount: int
    extras: list[str]
    locations: list[str]
    prorate: bool
    amenities: list[str]
    isRate: bool
    _id: str
    bookingPolicy: str
    name: str
    code: str
    account: str
    description: str
    rates: list[str]
    price: int
    organization: str
    createdAt: str
    createdBy: str


class ORNDResource(TypedDict):
    availability: list[ORNDResourceAvailability]
    _id: str
    price: int
    deposit: int
    parents: list[str]
    type: ORNDResourceType
    access: ORNDResourceAccess
    amenities: list[str]
    office: str
    name: str
    number: int
    size: int
    area: int
    rate: str
    organization: str
    createdAt: str
    modifiedAt: str
    createdBy: str
    modifiedBy: str
    color: str
    room: str
    target: str
    timezone: str
    status: str
    properties: dict[str, Union[str, int, float, bool, list[str]]]


class ORNDBookingRecurrence(TypedDict):
    rrule: Any


class ORNDServiceSlots(TypedDict):
    before: int
    after: int


class ORNDBookingDateTime(TypedDict):
    dateTime: str


class ORNDBookingFee(TypedDict):
    date: str
    formattedPrice: str
    member: str
    name: str
    office: str
    plan: str
    price: Union[int, float]
    quantity: int


class ORNDBookingFeeDetail(TypedDict):
    credits: list[str]
    date: str
    extraFees: list[str]
    fee: ORNDBookingFee
    valueCredits: list[str]


class ORNDBooking(TypedDict):
    office: str
    orgnaization: str
    resourceId: str
    reference: str
    start: ORNDBookingDateTime
    end: ORNDBookingDateTime
    accounted: bool
    tentative: bool
    accountedUntil: Optional[str]
    members: list[str]
    visitors: list[str]
    member: str
    team: str
    fees: list[ORNDBookingFeeDetail]
    canceled: bool
    recurrence: ORNDBookingRecurrence
    seriesStart: str
    seriesEnd: str
    summary: str
    source: str
    timezone: str
    serviceSlots: ORNDServiceSlots
    createdAt: str
    createdBy: str
    modifiedAt: str
    modifiedBy: str


class BookingIntervalAvailability(TypedDict):
    time: datetime
    available: bool


class ORNDLocation(TypedDict):
    name: str
    isOpen: bool
    country: Optional[str]
    state: Optional[str]
    city: Optional[str]
    address: Optional[str]
    zip: Optional[str]
    timezone: Optional[str]
    image: Optional[str]


class ORNDCompany(TypedDict):
    name: str
    office: ORNDLocation
    email: str
    createdAt: str
    createdBy: str
    modifiedAt: str
    modifiedBy: str


class ORNDUser(TypedDict):
    email: str
    name: str


class ORNDMember(TypedDict):
    _id: str
    name: str
    email: str
    phone: Optional[str]
    twitterHandle: Optional[str]
    team: Optional[str]
    contactPerson: Optional[bool]
    billingContact: Optional[bool]
    signedDocuments: list[str]
    office: ORNDLocation
    createdAt: str
    createdBy: str
    modifiedAt: str
    modifiedBy: str
    status: ORNDMemberStatus
    paymentDetails: list[str]


class ORNDAddress(TypedDict):
    address: str
    city: str
    zip: str
    state: str
    country: str
