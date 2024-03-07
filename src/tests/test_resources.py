import pytest
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from officerndapilib import (
    get_all_resources,
    get_resource_by_id,
    get_ornd_token,
)
from officerndapilib.schema import ORNDAuth

ORND_OFFICE_ID = "65416bf72db05a7176b467ac"

ORND_AUTH = ORNDAuth(
    client_id=os.getenv("ORND_CLIENT_ID", ""),
    client_secret=os.getenv("ORND_CLIENT_SECRET", ""),
    grant_type=os.getenv("ORND_GRANT_TYPE", ""),
    scope=os.getenv("ORND_SCOPE", ""),
    organization_slug="re-defined-test-account",
)


@pytest.fixture
def token():
    return get_ornd_token(ORND_AUTH)


def test_get_all_resources(token):
    resources = get_all_resources(
        token,
        ORND_OFFICE_ID,
        "team_room",
        queries=[("availableFrom", "2024-01-02"), ("type", "meeting_room")],
    )
    pprint(resources, indent=2, width=120)
    assert isinstance(resources, list)
    assert len(resources) > 0


def test_get_resource_by_id():
    resource_id = "65c38ead5e6d7bd36ed6a540"  # LGC
    resource = get_resource_by_id(resource_id)
    pprint(resource, indent=2, width=120)
    assert resource["_id"] == resource_id
