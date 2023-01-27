import unittest
from database.class_project import ProjectType

from flaskr.visit_routes import SignoutRequest
import datetime as dt

class TestSignoutRequestSerialization(unittest.TestCase):

    def test_deserialize_empty(self):
        req = SignoutRequest.from_dict({})
        self.assertEqual([], req.np_worksession)
        self.assertEqual([], req.ep_worksession)

    def test_deserialize_new_project(self):
        req = SignoutRequest.from_dict({
            "newProjectWorkSessions": [
                {
                    "project": {
                        "name": "Foobar",
                        "type": "Personal",
                        "description": "A fun Project",
                    },
                    "equipmentUseLog": [
                        {
                            "equipmentId":  15,
                            "timeUsed": 350, # Duration in seconds
                            "consumedMaterial": [
                                {
                                    "materialId": 20,
                                    "quantity": 30.0,
                                    "units": "in",
                                }
                            ]
                        }
                    ],
                }
            ]
        })
        self.assertEqual(len(req.np_worksession), 1)

        work_session = req.np_worksession[0]
        self.assertEqual("Foobar", work_session.project.name)
        self.assertEqual(ProjectType.Personal, work_session.project.type)
        self.assertEqual("A fun Project", work_session.project.description)

        self.assertEqual(15, work_session.equipment_use_log[0].equipment_id)
        self.assertEqual(dt.timedelta(seconds=350), work_session.equipment_use_log[0].time_used)
        self.assertEqual(20, work_session.equipment_use_log[0].consumed_material[0].material_id)
        self.assertEqual(30.0, work_session.equipment_use_log[0].consumed_material[0].quantity)
        self.assertEqual("in", work_session.equipment_use_log[0].consumed_material[0].units)


        
    def test_deserialize_existing_project(self):
        req = SignoutRequest.from_dict({
            "existingProjectWorkSessions": [
                {
                    "projectId": 15,
                    "equipmentUseLog": [
                        {
                            "equipmentId":  15,
                            "timeUsed": 350, # Duration in seconds
                            "consumedMaterial": [
                                {
                                    "materialId": 20,
                                    "quantity": 30.0,
                                    "units": "in",
                                }
                            ]
                        }
                    ],
                }
            ]
        })
        self.assertEqual(len(req.ep_worksession), 1)
        self.assertEqual(15, req.ep_worksession[0].project_id)

        work_session = req.ep_worksession[0]
        self.assertEqual(15, work_session.equipment_use_log[0].equipment_id)
        self.assertEqual(dt.timedelta(seconds=350), work_session.equipment_use_log[0].time_used)
        self.assertEqual(20, work_session.equipment_use_log[0].consumed_material[0].material_id)
        self.assertEqual(30.0, work_session.equipment_use_log[0].consumed_material[0].quantity)
        self.assertEqual("in", work_session.equipment_use_log[0].consumed_material[0].units)
        
