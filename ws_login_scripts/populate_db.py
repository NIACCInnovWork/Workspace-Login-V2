""" This script generates fake data for testing how the system behaves with 
more data
"""
from faker import Faker
import datetime as dt

from ws_login_domain import User, UserType
from ws_login_client import ApiClient


class UserFactory:
    """ Provides an iterator of new users up to the count supplied.

    Each new user is created using the POST:/api/users api call so ensures the 
    user exists within the service before returning.

    Every user generated will have a unique name which did not previously exist
    within the system.
    """
    def __init__(self, api_client: ApiClient, faker: Faker, count: int = 100):
        self.api_client = api_client
        self.faker = faker
        self.count = count

    def __iter__(self):
        return self

    def __next__(self) -> User:
        if not self.count:
            raise StopIteration()
        self.count -= 1

        new_name = self.faker.name()
        while self.api_client.get_users(name=new_name):
            new_name = self.faker.name()

        date_joined = self.faker.date_between(dt.datetime(2022, 1, 1), dt.datetime.now())
        return self.api_client.create_user(new_name, self.faker.enum(UserType), date_joined)


def main():
    # api_client = ApiClient("https://dev.workspace-login.riesenlabs.com", "*****")
    api_client = ApiClient("http://localhost:5000", "test-token")
    for user in UserFactory(api_client, Faker()):
    #     # Generate Some Visits
    #         # Select or create a project
    #             # Equiptment Usage
        print(user)

if __name__ == "__main__":
    main()
