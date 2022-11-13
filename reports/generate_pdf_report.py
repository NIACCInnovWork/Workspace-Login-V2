"""
This file is to be replaced with the newer generate_KPI_report file.
"""

import os
import shutil
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
from fpdf import FPDF

import matplotlib.pyplot as plt
from matplotlib import rcParams
import mysql.connector

from reports.total_report import generate_total_report

rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False

PLOT_DIR = 'plots'


def construct_pdf(mydb: mysql.connector):
    # Delete folder if exists and create it again
    try:
        shutil.rmtree(PLOT_DIR)
        os.mkdir(PLOT_DIR)
    except FileNotFoundError:
        os.mkdir(PLOT_DIR)

    generate_total_report(mydb)

    counter = 0
    pages_data = []
    temp = []
    # Get all plots
    files = os.listdir(PLOT_DIR)

    # Page One
    temp.append(f'{PLOT_DIR}/User Type Histogram.png')
    temp.append(f'{PLOT_DIR}/User Type Pie Chart.png')
    pages_data.append(temp)

    return [*pages_data, temp]


class ReportPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.WIDTH = 210
        self.HEIGHT = 297

    def header(self):
        # Custom Logo and Positioning
        # Create a 'resources' folder and put any wide and short images inside
        self.image('resources/Innovation Workspace Logo-Official-Scaled.png', 10, 8, 33)
        self.set_font('Arial', 'B', 11)
        self.cell(self.WIDTH - 80)
        self.cell(60, 1, 'Sales Report', 0, 0, 'R')
        self.ln(20)

    def footer(self):
        # Page numbers in the footer
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def page_body(self, images):
        # Determine how many plots there are per page and set positions and margins accordingly
        self.cell(0, 10, 'Total Workspace Data', 0, 0, 'C')
        if len(images) == 3:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            print(images[0])
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
            self.image(images[2], 15, self.WIDTH / 2 + 90, self.WIDTH - 30)
        elif len(images) == 2:
            self.image(images[0], 15, 25, self.WIDTH - 30)
            self.image(images[1], 15, self.WIDTH / 2 + 5, self.WIDTH - 30)
        else:
            self.image(images[0], 15, 25, self.WIDTH - 30)

    def print_page(self, images):
        # Add pages to the PDF document
        self.add_page()
        self.page_body(images)


def generate_full_report(mydb: mysql.connector):
    # Function to create a report
    plots_per_page = construct_pdf(mydb)  # Call & compile all plots
    pdf = ReportPDF()
    pdf.set_title('Total Data Report')
    for elem in plots_per_page:  # Iterate over the pages
        pdf.print_page(elem)  # add a page to the pdf
    pdf.output('exported_reports/Workspace_Total_Report.pdf', 'F')  # Output the PDF document
