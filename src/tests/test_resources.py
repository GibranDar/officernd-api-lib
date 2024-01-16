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
    resource_id = "633c10e732747f9706f87681"
    resource = get_resource_by_id(resource_id)
    pprint(resource, indent=2, width=120)
    assert resource["_id"] == resource_id
