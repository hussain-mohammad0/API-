import requests_mock
import pytest
import requests
import uuid
from API_DATA import get_people
from API_DATA import create_contact
from API_DATA import clean_name
from API_DATA import transform_data


def test_get_people():
    # mock the response of the GET /people/ API endpoint
    with requests_mock.Mocker() as mock:
        mock.get("https://link/people/", status_code=200, json=[{
            "fields": {
                "firstName": "John",
                "lastName": "Doe",
                "dateOfBirth": "01-01-2000",
                "email": "john.doe@example.com",
                "lifetimeValue": "$100.00"
            }
        }])
        people = get_people()
        # assert that the response is correct
        assert people == [{
            "fields": {
                "firstName": "John",
                "lastName": "Doe",
                "dateOfBirth": "01-01-2000",
                "email": "john.doe@example.com",
                "lifetimeValue": "$100.00"
            }
        }]

def test_create_contact():
    # mock the response of the POST /contacts/ API endpoint
    with requests_mock.Mocker() as mock:
        mock.post("https://link/contacts/", status_code=200, json={
            "first_name": "John",
            "last_name": "Doe",
            "birthdate": "2000-01-01",
            "email": "john.doe@example.com",
            "custom_properties": {
                "airtable_id": "abc123",
                "lifetime_value": 100.00
            }
        })
        contact = {
            "first_name": "John",
            "last_name": "Doe",
            "birthdate": "2000-01-01",
            "email": "john.doe@example.com",
            "custom_properties": {
                "airtable_id": "abc123",
                "lifetime_value": 100.00
            }
        }
        created_contact = create_contact(contact)
        # assert that the response is correct
        assert created_contact == {
            "first_name": "John",
            "last_name": "Doe",
            "birthdate": "2000-01-01",
            "email": "john.doe@example.com",
            "custom_properties": {
                "airtable_id": "abc123",
                "lifetime_value": 100.00
            }
        }



def transform_data(people):
    # Transform the data to match the Contact object schema
    contacts = []
    for person in people:
        lifetime_value = 0.0
        if "lifetimeValue" in person["fields"]:
            lifetime_value = float(person["fields"]["lifetimeValue"].strip("$"))

        contact = {
            "first_name": clean_name(person["fields"]["firstName"]),
            "last_name": clean_name(person["fields"]["lastName"]),
            "birthdate": datetime.datetime.strptime(person["fields"]["dateOfBirth"], "%d-%m-%Y").strftime("%Y-%m-%d"),
            "email": person["fields"]["email"],
            "custom_properties": {
                "airtable_id": str(uuid.uuid1()),
                "lifetime_value": lifetime_value
            }
        }
        contacts.append(contact)
    return contacts


def test_clean_name():
    # Test case 1: Check if leading and trailing spaces are removed from first & last names
    name = "   John Doe   "
    result = clean_name(name)
    assert result == "John Doe", f"Expected 'John Doe', but got {result}"

    # Test case 2: Check if only leading spaces are removed from first & last names
    name = "   John Doe"
    result = clean_name(name)
    assert result == "John Doe", f"Expected 'John Doe', but got {result}"

    # Test case 3: Check if only trailing spaces are removed from first & last names
    name = "John Doe   "
    result = clean_name(name)
    assert result == "John Doe", f"Expected 'John Doe', but got {result}"

    # Test case 4: Check if no spaces are removed from first & last names
    name = "John Doe"
    result = clean_name(name)
    assert result == "John Doe", f"Expected 'John Doe', but got {result}"
