from typing import List, Optional, Dict
import datetime as dt

from ws_login_domain import * 
from ws_login_domain.requests import SignoutRequest

import requests


class UnknownStatError(Exception):
    pass

class ApiClient:
    def __init__(self, root_url, api_token: str):
        """ Provides python wrapper around access to the workspace REST api
        :param: root_url the location at which the service is located
        """
        self.root_url = root_url
        self.session = requests.Session()
        self.session.cookies = requests.cookies.cookiejar_from_dict({"api-token": api_token})

    def close(self):
        self.session.close()

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
            date_joined = dt.datetime.fromisoformat(resp["dateJoined"]),
            user_type = UserType[resp["userType"]],
        )

    def create_user(self, name: str, user_type: UserType, date_joined: Optional[dt.datetime]):
        new_user_req = {
            "name": name, 
            "type": user_type.name,
        }
        if date_joined:
            new_user_req["dateJoined"] = date_joined.isoformat()

        resp = self.session.post(f"{self.root_url}/api/users", json=new_user_req)
        resp_json = resp.json()
        return User(
            user_id = resp_json["userId"],
            name = resp_json["name"],
            date_joined = dt.datetime.fromisoformat(resp_json["dateJoined"]),
            user_type = UserType[resp_json["userType"]],
        )
    
    def get_visits(self) -> List[Visit]:
        req = self.session.get(f"{self.root_url}/api/visits")
        # TODO no error checking right now
        resp = req.json()
        return [
            Visit(item["id"], item["userId"], item["startTime"], item["endTime"])
            for item in resp
        ]


    def get_visits_for(self, user: User, ongoing=None):
        params = {}
        if ongoing is not None:
            params["ongoing"] = str(ongoing).lower()
        req = self.session.get(f"{self.root_url}/api/users/{user.user_id}/visits", params=params)
        # TODO no error checking right now
        resp = req.json()

        return [
            Visit(
                item["id"], 
                user.user_id, 
                dt.datetime.fromisoformat(item["startTime"]),
                dt.datetime.fromisoformat(item["endTime"]) if item.get("endTime") else None, 
            )
            for item in resp
        ]
    

    def create_visit_for(self, user: User, start_time: Optional[dt.datetime] = None) -> Visit:
        req_body = { "startTime": start_time.isoformat() } if start_time else {}
        req = self.session.post(f"{self.root_url}/api/users/{user.user_id}/visits", json=req_body)
        # TODO no error checking right now
        item = req.json()
        return Visit(
            item["id"], 
            user.user_id, 
            dt.datetime.fromisoformat(item["startTime"]), 
            None, # always none if visit was just created
        )

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
            return Project(rec["id"], rec["name"], rec["description"], ProjectType[rec["type"]]) 
        except requests.exceptions.JSONDecodeError as ex:
            print("Failed Request Text")
            print(req.text)
            raise ex

    def get_projects_for(self, user: User) -> List[ProjectSummary]:
        req = self.session.get(f"{self.root_url}/api/users/{user.user_id}/projects")
        return [ProjectSummary(rec["id"], rec["name"]) for rec in req.json()]

    def signout(self, signout_request: SignoutRequest):
        resp = self.session.post(
                f"{self.root_url}/api/visits/{signout_request.visit_id}/_signout", json=signout_request.to_dict()
        )
        resp.raise_for_status()

    def get_stats(self) -> List[str]:
        req = self.session.get(f"{self.root_url}/api/stats")
        return [ stat for stat in req.json().keys() ]

    def get_stat(self, stat_name: str) -> List[Dict]: 
        # NOTE im unsure if this should use raw dictionarys or the Scaler / 
        # Pointer types the server uses. This is only used for integration 
        # testing for now, so we will leave it as just Dicts
        req = self.session.get(f"{self.root_url}/api/stats/{stat_name}")
        if req.status_code == 404:
            raise UnknownStatError("Could not find stat " + stat_name)
        return req.json()


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
