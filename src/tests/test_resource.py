import pytest
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from officerndapilib import get_all_resources, get_resource_by_id


def test_get_all_resources():
    office_id = os.getenv("ORND_OFFICE_ID", "")
    resources = get_all_resources(
        office_id,
        "team_room",
        queries=[("availableFrom", "2024-01-02")],
    )
    pprint(resources, indent=2, width=120)
    assert isinstance(resources, list)
    assert len(resources) > 0


def test_get_resource_by_id():
    resource_id = "639b43cd3add2ed1008582ae"  # Suite G.02
    resource = get_resource_by_id(resource_id)
    pprint(resource, indent=2, width=120)
    assert resource["_id"] == resource_id
