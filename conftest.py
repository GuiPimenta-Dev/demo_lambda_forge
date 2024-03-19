import json
import os
import moto
import boto3
import pytest


@pytest.fixture
def env():
    os.environ["USERS_TABLE"] = "USERS_TABLE"


@pytest.fixture
def users_table(env):
    with moto.mock_dynamodb():
        db = boto3.client("dynamodb")
        db.create_table(
            AttributeDefinitions=[
                {"AttributeName": "PK", "AttributeType": "S"},
            ],
            TableName="USERS_TABLE",
            KeySchema=[
                {"AttributeName": "PK", "KeyType": "HASH"},
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        table = boto3.resource("dynamodb").Table("USERS_TABLE")
        yield table


def pytest_generate_tests(metafunc):
    for mark in metafunc.definition.iter_markers(name="integration"):
        with open(".tested_endpoints.jsonl", "a") as f:
            f.write(f"{json.dumps(mark.kwargs)}\n")
