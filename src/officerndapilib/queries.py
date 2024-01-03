from typing import Literal, TypeVar, Union

# QUERIES

## base query types

P = TypeVar("P")

ORNDNameQueryParams = Literal[
    "name",
    "name.$sw",  # starts with
    "name.$swi",
    "name.$ew",  # ends with
    "name.$ewi",
    "name.$cs",  # contains
    "name.$csi",
]

ORNDPagingQueryParams = Literal[
    "$limit",
    "$next",
    "$prev",
]

ORNDTimingQueryParams = Literal[
    "createdAt.$gt",  # greater than
    "createdAt.$lt",  # less than
    "modifiedAt.$gt",
    "modifiedAt.$lt",
]

ORNDBaseQueryParams = Union[
    ORNDNameQueryParams,
    ORNDPagingQueryParams,
    ORNDTimingQueryParams,
    Literal["$sort"],
]

## specific query types

Q = TypeVar("Q")

ORNDResourceQueryParams = Union[
    ORNDNameQueryParams,
    Literal["type", "availableFrom", "availableTo", "office"],
]
ORNDCompanyQueryParams = Union[
    ORNDNameQueryParams, ORNDBaseQueryParams, Literal["office"]
]
ORNDMemberQueryParams = Union[
    ORNDNameQueryParams, ORNDBaseQueryParams, Literal["team", "office"]
]

ORNDBaseQuery = tuple[Union[P, Q], str]
ORNDResourceQuery = ORNDBaseQuery[ORNDNameQueryParams, ORNDResourceQueryParams]
ORNDCompanyQuery = ORNDBaseQuery[ORNDBaseQueryParams, ORNDCompanyQueryParams]
ORNDMemberQuery = ORNDBaseQuery[ORNDBaseQueryParams, ORNDMemberQueryParams]


def append_queries_to_url(url: str, queries: list[ORNDBaseQuery]):
    if url[-1] != "?":
        url += "?"
    for i, qv in enumerate(queries):
        q = qv[0]
        v = qv[1]
        if i == 0:
            url += f"{q}={v}"
        else:
            url += f"&{q}={v}"
    return url
