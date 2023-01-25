import requests
from database.class_user import User, UserSummary, UserType
from database.class_visit import Visit
from database.class_equipment import Equipment
from database.class_material import Material
from database.class_project import Project, ProjectSummary, ProjectType
from typing import List, Optional

from flaskr.visit_routes import SignoutRequest

class ApiClient:
    def __init__(self, root_url, api_token: str):
        """ Provides python wrapper around access to the workspace REST api
        :param: root_url the location at which the service is located
        """
        self.root_url = root_url
        self.session = requests.Session()
        self.session.cookies = requests.cookies.cookiejar_from_dict({"api-token": api_token})

    def get_users(self, name: Optional[str] = None, ongoing=None) -> List[UserSummary]:
        params = {}
        if name is not None:
            params["name"] = name
        if ongoing is not None:
            params["ongoing"] = str(ongoing).lower()

        req = self.session.get(f"{self.root_url}/api/users", params=params)
        # TODO no error checking right now
        return [UserSummary(rec["id"], rec["name"]) for rec in req.json()]

    def get_user(self, user_id: int) -> User:
        req = self.session.get(f"{self.root_url}/api/users/{user_id}")
        # TODO no error checking right now
        resp = req.json()
        return User(
            user_id = resp["userId"],
            name = resp["name"],
            date_joined = resp["dateJoined"],
            user_type = UserType[resp["userType"]],
        )

    def create_user(self, name: str, user_type: UserType):
        req = self.session.post(f"{self.root_url}/api/users", 
            json={
                "name": name, 
                "type": user_type.name,
            }
        )
        resp = req.json()
        return User(
            user_id = resp["userId"],
            name = resp["name"],
            date_joined = resp["dateJoined"],
            user_type = UserType[resp["userType"]],
        )

    def get_visits_for(self, user: User, ongoing=None):
        params = {}
        if ongoing is not None:
            params["ongoing"] = str(ongoing).lower()
        req = self.session.get(f"{self.root_url}/api/users/{user.user_id}/visits", params=params)
        # TODO no error checking right now
        resp = req.json()
        return [
            Visit(item["id"], user.user_id, item["startTime"], item["endTime"])
            for item in resp
        ]
    

    def create_visit_for(self, user: User) -> Visit:
        req = self.session.post(f"{self.root_url}/api/users/{user.user_id}/visits")
        # TODO no error checking right now
        item = req.json()
        return Visit(item["id"], user.user_id, item["startTime"], item["endTime"])

    def get_equipment(self) -> List[Equipment]:
        req = self.session.get(f"{self.root_url}/api/equipment")
        items = req.json()
        return [ Equipment(item["id"], item["name"]) for item in items ]

    def get_materials_for(self, eq: Equipment) -> List[Material]:
        req = self.session.get(f"{self.root_url}/api/equipment/{eq.equipment_id}/materials")
        items = req.json()
        return [ Material(item["id"], item["name"], item["unit"]) for item in items ]

    def get_projects(self) -> List[ProjectSummary]:
        req = self.session.get(f"{self.root_url}/api/projects")
        return [ProjectSummary(rec["id"], rec["name"]) for rec in req.json()]

    def get_project(self, project_id: int) -> Optional[Project]:
        req = self.session.get(f"{self.root_url}/api/projects/{project_id}")
        try:
            rec = req.json()
            print(rec)
            return Project(rec["id"], rec["name"], rec["description"], ProjectType[rec["type"]]) 
        except requests.exceptions.JSONDecodeError as ex:
            print("Failed Request Text")
            print(req.text)
            raise ex

    def get_projects_for(self, user: User) -> List[ProjectSummary]:
        req = self.session.get(f"{self.root_url}/api/users/{user.user_id}/projects")
        return [ProjectSummary(rec["id"], rec["name"]) for rec in req.json()]

    def signout(self, signout_request: SignoutRequest):
        print("Sending Signout Request")
        resp = self.session.post(
                f"{self.root_url}/api/visits/{signout_request.visit_id}/_signout", json=signout_request.to_dict()
        )
        resp.raise_for_status()
        

if __name__ == '__main__':
    # client = ApiClient('http://workspace-login.riesenlabs.com')
    client = ApiClient('http://localhost:5000')
    # print(client.get_users(ongoing=False))
    # print(client.create_user(name="fred", user_type=UserType.Staff))
    print(client.get_equipment())
    # user = client.get_user(3)
    # print(user)
    #
    # print(client.get_visits_for(user))
