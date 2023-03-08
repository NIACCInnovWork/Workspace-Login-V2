""" This script generates fake data for testing how the system behaves with 
more data
"""
from faker import Faker
import random
import datetime as dt
import os
from typing import List
from dataclasses import dataclass

from ws_login_scripts.utils import exit_with
from ws_login_domain import User, UserType, Equipment, Material, Visit, ProjectType
from ws_login_domain.requests import SignoutRequest
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


@dataclass
class EquipmentAndMaterials:
    """ Tuple for containing equipment and the list of materials this equipment 
    could possibly consume
    """
    equipment: Equipment
    material: List[Material]


def fetch_equipment_and_materials(client: ApiClient) -> List[EquipmentAndMaterials]:
    """ Fetches all equipment currently in the system and the materials each 
    equipment can use.

    Values are returned as an EquipmentAndMaterials objects. 

    This function will pull all data without bounds and assumes the data 
    fetched is small enough to fit in memory.

    WARNING: This function will trigger a LOT of api calls.

    """
    ret_list = []
    for eq in client.get_equipment():
        ret_list.append(EquipmentAndMaterials(eq, client.get_materials_for(eq)))
    return ret_list


def generate_visit_for_user(
        client: ApiClient, 
        faker: Faker, 
        eq_and_mat: List[EquipmentAndMaterials], 
        user: User
    ):
    """ Generates a visit for a user

    The visit start time is randomly picked between when the user joins the 
    system and the current time.  The signout time is picked between when visit 
    starts and the end of that day.

    A new random project is created for the visit, and a one equipment usage 
    log is generated for the new project work session.
    """
    start_time = faker.date_time_between(user.date_joined, dt.datetime.now())
    visit = client.create_visit_for(user, start_time)

    end_time = faker.date_time_between(visit.start_time, dt.datetime.combine(visit.start_time.date(), dt.datetime.max.time()))
    signout_req = SignoutRequest.for_visit(visit, end_time)

    # TODO:
    # - [ ] Multiple visits for the same project
    # - [ ] Collaboration with others on there project
    # - [ ] Multiple pieces of equipment used per project

    worksession = signout_req.with_new_project(
            faker.sentence(nb_words=6), 
            faker.paragraph(), 
            faker.enum(ProjectType)
    )

    equipment_and_mat = random.choice(eq_and_mat)

    # FIXME! nothing here says the use time is shorter than the visit time
    # Question for anthony, Maybe that is ok? if someone starts a job and then 
    # leaves?
    work_log = worksession.with_equipment_use(
            equipment_and_mat.equipment, 
            dt.timedelta(seconds=random.randint(60, 4*60))
    )

    mat = random.choice(equipment_and_mat.material)
    quantity = random.randint(50, 500) if mat.material_name != "N/A" else 0
    work_log.with_consumed_materials(mat, quantity)

    client.signout(signout_req)


def main():
    api_token = os.environ.get("API_TOKEN")
    if not api_token:
        exit_with("No api token set in API_TOKEN env var")

    api_client = ApiClient("https://dev.workspace-login.riesenlabs.com", api_token)
    # api_client = ApiClient("http://localhost:5000", "test-token")
    eq_and_mat = fetch_equipment_and_materials(api_client)

    faker = Faker()
    for user in UserFactory(api_client, faker):
        generate_visit_for_user(api_client, faker, eq_and_mat, user)
        print(f'created user: {user.name}')


if __name__ == "__main__":
    main()
