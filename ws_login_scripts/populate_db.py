""" This script generates fake data for testing how the system behaves with 
large quantities of data.

The script is currently hard-coded to point at the dev database, but expects an 
api token to be provided in the environment variable API_TOKEN.

The script will generate 100 new users and for each of them add between 3 and 
15 visits for each user.  Additionally, each user can have up to 3 projects 
generated. Roughly 10% of projects should have more than one user join them. 
Currently all of these values are hard coded and not configurable by the script 
invoker.

The script can be run using the command:
>>> python -m ws_login_scripts.populate_db

"""
from faker import Faker
import random
import datetime as dt
import os
from typing import List
from dataclasses import dataclass

from ws_login_scripts.utils import exit_with, continue_prompt
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


def generate_worksession(client: ApiClient, faker: Faker, req: SignoutRequest, user: User):
    """ Generates a new worksession on the provided signout request.

    The service will be queried to see if this user is associated with any 
    existing projects. If so, one of those projects will be used.  If no 
    project is found, a new project is created in stead.

    Additionally, there is a 10% chance that all projects will be queried 
    instead and the user added to an existing project which is not there own.
    """
    # Generate New Project
    project_sum = []
    if faker.boolean(10):
        project_sum = client.get_projects()
    else:
        project_sum = client.get_projects_for(user)

    if project_sum:
        # Found Existing project
        project = client.get_project(random.choice(project_sum))
        return req.with_existing_project(project)
    else:
        # No existing project found. Create one
        return req.with_new_project(
                faker.sentence(nb_words=6), 
                faker.paragraph(), 
                faker.enum(ProjectType)
        )


def generate_equipment_usage_log(eq_and_mat, worksession):
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

    for _ in range(random.randint(1, 3)):
        # Worked on a random number of projects between 1 and 3
        worksession = generate_worksession(client, faker, signout_req, user)

        for _ in range(random.randint(1, 3)):
            # Used a random piece of equipment between 1 and 3
            generate_equipment_usage_log(eq_and_mat, worksession)
    
    # Send signout request
    client.signout(signout_req)


def main():
    """ Main entrypoint into script
    """
    api_token = os.environ.get("API_TOKEN")
    if not api_token:
        exit_with("No api token set in API_TOKEN env var")

    print(
        "This utility will generate a buch of fake data and send it to the "
        "service.  The utility doesn't delete any data, but the the script "
        "will establish relationships between new users and existing projects "
        "making existing data tricky to isolate."
        ""
        "The utility will generate 100 new users with between 3-15 visits per "
        "user."
    )
    continue_prompt("Are you sure you want to continue?")

    api_client = ApiClient("https://dev.workspace-login.riesenlabs.com", api_token)
    # api_client = ApiClient("http://localhost:5000", "test-token")
    eq_and_mat = fetch_equipment_and_materials(api_client)

    faker = Faker()
    for user in UserFactory(api_client, faker):
        print(f'created user: {user.name}')
        for _ in range(random.randint(3, 15)):
            generate_visit_for_user(api_client, faker, eq_and_mat, user)
            print(f'generated visit')


if __name__ == "__main__":
    main()
