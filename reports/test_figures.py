import unittest
from unittest.mock import Mock
import pandas as pd

from reports.figures import FigureService

# These functions test the plot ouput functions.  Unfortunantely, because
# the plots are pngs, querying that the plot itself is correct is proibitivly
# tricky. The tests can only verify that a plot was successfully generated
# given the input, and not that the plot itself is correct

class TestCreateUserTypePiChart(unittest.TestCase):
    def setUp(self):
        self.fig_srv = FigureService(Mock())

    def test_empty_dataframe_generates_figure(self):
        data = pd.DataFrame([], columns=['user_type'])
        figure = self.fig_srv.create_user_type_histogram(data)
        self.assertIsNotNone(figure)
        self.assertTrue(figure.filepath.exists())

    def test_empty_dataframe_with_data_generates_figure(self):
        data = pd.DataFrame(['Student', 'Staff', 'Staff', 'Staff'], columns=['user_type'])
        figure = self.fig_srv.create_user_type_histogram(data)
        self.assertIsNotNone(figure)
        self.assertTrue(figure.filepath.exists())

class TestCreateUserTypePyChart(unittest.TestCase):
    def setUp(self):
        self.fig_srv = FigureService(Mock())

    def test_empty_datafraome_generates_figure(self):
        data = pd.DataFrame([], columns=['user_type'])
        figure = self.fig_srv.create_user_type_pie_chart(data)
        self.assertIsNotNone(figure)
        self.assertTrue(figure.filepath.exists())
    
    def test_empty_dataframe_with_data_generates_figure(self):
        data = pd.DataFrame(['Student', 'Staff', 'Staff', 'Staff'], columns=['user_type'])
        figure = self.fig_srv.create_user_type_pie_chart(data)
        self.assertIsNotNone(figure)
        self.assertTrue(figure.filepath.exists())

class TestCreateVisitHeatMap(unittest.TestCase):
    def setUp(self):
        self.fig_srv = FigureService(Mock())

    def test_empty_datafraome_generates_figure(self):
        data = pd.DataFrame([[pd.Timestamp(2020,1,1), pd.Timestamp(2020,1,1)]], columns=['start_time', 'end_time'])
        figure = self.fig_srv.create_visit_heat_map(data)
        self.assertIsNotNone(figure)
        self.assertTrue(figure.filepath.exists())
