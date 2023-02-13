import requests
import datetime

def get_people():
    # Call the GET /people/ API endpoint
    headers = {"Authorization": "Bearer abcdef123456"}
    response = requests.get("https://link/people/", headers=headers)

    # Check if the request is successful
    if response.status_code == 200:
        people = response.json()
        return people
    else:
        raise Exception("Failed to get people data.")

def create_contact(contact):
    # Call the POST /contacts/ API endpoint
    headers = {"Content-Type": "application/json"}
    auth = requests.auth.HTTPBasicAuth("datacose", "123456789")
    response = requests.post("https://link/contacts/", headers=headers, auth=auth, json=contact)

    # Check if the request is successful
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to create contact.")

def clean_name(name):
    # Remove leading and trailing spaces from first & last names
    return name.strip()

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
                "airtable_id": person["id"],
                "lifetime_value": lifetime_value
            }
        }
        contacts.append(contact)
    return contacts


def main():
    people = get_people()
    contacts = transform_data(people)

    # POST each Contact to the /contacts/ API endpoint
    for contact in contacts:
        created_contact = create_contact(contact)
        print(f"Successfully created contact: {created_contact}")

if __name__ == "__main__":
    main()

