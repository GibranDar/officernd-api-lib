import pytest
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from officerndapilib import (
    get_ornd_token,
    create_member,
    get_all_members,
    get_member_by_email,
    delete_members,
)
from officerndapilib.schema import ORNDAuth
from officerndapilib.reqs import CreateORNDMemberRequest

ORND_AUTH = ORNDAuth(
    client_id=os.getenv("ORND_CLIENT_ID", ""),
    client_secret=os.getenv("ORND_CLIENT_SECRET", ""),
    grant_type=os.getenv("ORND_GRANT_TYPE", ""),
    scope=os.getenv("ORND_SCOPE", ""),
    organization_slug="re-defined-test-account",
)

ORND_ORGANIZATION = os.getenv("ORND_ORG_SLUG", "")

WW_12MOORGATE = "65416bf72db05a7176b467ac"
LRH = "633ac05fb85f276bea3f644b"

TEST_MEMBER_NAME = "Test Member 1"
TEST_MEMBER_EMAIL = "testmember1@gmail.com"
TEST_MEMBER_PHONE = "07426389643"


@pytest.fixture
def token():
    return get_ornd_token(ORND_AUTH)


def test_create_member(token):
    member_request = CreateORNDMemberRequest(
        startDate="2024-01-01T00:00:00Z",
        office=WW_12MOORGATE,
        name=TEST_MEMBER_NAME,
        email=TEST_MEMBER_EMAIL,
        phone=TEST_MEMBER_PHONE,
        description="",
        properties={},
        address={},
    )
    member = create_member(token, ORND_ORGANIZATION, member_request)
    pprint(member, indent=2, width=120)
    assert member[0].get("_id")
    assert member[0]["name"] == TEST_MEMBER_NAME
    assert member[0]["email"] == TEST_MEMBER_EMAIL
    assert member[0]["phone"] == TEST_MEMBER_PHONE


def test_get_all_members(token):
    members = get_all_members(token, ORND_ORGANIZATION, WW_12MOORGATE)
    assert len(members) > 0


def test_get_member_by_email(token):
    member = get_member_by_email(
        token, ORND_ORGANIZATION, WW_12MOORGATE, TEST_MEMBER_EMAIL
    )
    pprint(member, indent=2, width=120)
    assert member["email"] == TEST_MEMBER_EMAIL


def test_delete_members(token):
    member = get_member_by_email(
        token, ORND_ORGANIZATION, WW_12MOORGATE, TEST_MEMBER_EMAIL
    )
    member_ids = [member["_id"]]
    deleted_members = delete_members(token, ORND_ORGANIZATION, member_ids)
    pprint(deleted_members, indent=2, width=120)
    assert len(deleted_members) == len(member_ids)
    for deleted in deleted_members:
        assert deleted["_id"] in member_ids
