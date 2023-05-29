"""
Extension of FPDF class for the creation and export of Key Performance Indicators Report using data collected in the
main application.
"""
from typing import List
from fpdf import FPDF

from ws_login_reports.figures import Figure, FigureService
from PIL import Image
import datetime as dt

title = 'Usage Report'
section_1 = 'Visitor Statistics'
section_2 = 'Project Statistics'
section_3 = 'Equipment Statistics'


class PDF(FPDF):
    """
    Extend the normal PDF class for customized header, footer, and chapter definitions
    """
    def header(self):
        """
        Create Header with Workspace Logo and Document Title
        """
        # logo -- Setting height keeps proportions uniform
        self.image('resources/Innovation Workspace Logo-Official-Scaled.png', 10, 8, 75)
        # font
        self.set_font('helvetica', 'B', 20)
        # Title
        self.cell(0, 10, title, border=0, ln=0, align='R')
        # Line Break
        self.ln(20)

    def footer(self):
        """
        Create footer with page number.
        """
        # Set position of footer
        self.set_y(-15)
        # Set font
        self.set_font('helvetica', 'I', 10)
        # Page Number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    # # Adding chapter title to the start of each chapter
    # def chapter_title(self, ch_num, ch_title, link):
    #     """
    #     Create 'chapter titles' for each section that splits the document into readable chunks
    #     :param ch_num: Section Number (numeral)
    #     :param ch_title: Section Title
    #     :param link: Link to allow for internal hyperlinks and interactive table of contents
    #     :return: None
    #     """
    #     # Set Link Location
    #     self.set_link(link)
    #     # set font
    #     self.set_font('helvetica', '', 12)
    #     # set background color
    #     self.set_fill_color(200, 220, 255)
    #     # Chapter Title
    #     chapter_title = f'Chapter {ch_num} : {ch_title}'
    #     self.cell(0, 5, chapter_title, ln=1, fill=1)
    #     # Line Break
    #     self.ln()
    #
    # # Chapter content
    # def chapter_body(self, name, figure):
    #     """
    #     This method is used to construct each "chapter" or section in the PDF report. This method will take in a
    #     description text file followed by a list of graphics and descriptions that comprise the content for the section.
    #     :param name:
    #     :return:
    #     """
    #     # read Section_1_Description.txt file
    #     with open (name, 'rb') as fh:
    #         txt = fh.read().decode('latin-1')
    #     # Set font
    #     self.set_font('times', '', 12)
    #     # insert Section_1_Description.txt
    #     self.multi_cell(0, 5, txt, border=1)
    #     # line break
    #     self.ln()
    #
    #     # Initially format a single Plot
    #     image_height = self.h
    #     self.image(str(figure.filepath), x=10, y=60, w=self.w / 2.5)
    #     # self.image(r"plots/User_Type_Histogram.png", x=self.w / 2, y=60, w=self.w / 2.5)
    #
    #     self.cell(0, 5, 'Test Adding Additional Text', ln=1)
    #
    #     # End each chapter
    #     self.set_font('times', 'I', 12)
    #     self.cell(0, 5, 'END OF CHAPTER')
    #
    # def print_chapter(self, ch_num, ch_title, name, link, figure):
    #     """
    #     Method that adds a page for the beginning of each chapter, invokes chapter_title method and chapter_body method.
    #     :param ch_num: Chapter Number (numeral)
    #     :param ch_title: Section Title
    #     :param name: Chapter Name # ToDo - seems to be redundancy here; check to see if it can be cleaned up.
    #     :param link:
    #     :return:
    #     """
    #     self.add_page()
    #     self.chapter_title(ch_num, ch_title, link)
    #     self.chapter_body(name, figure)


class Section:
    def __init__(self, title: str):
        self.title = title
        self.text = []
        self.figures = []

    def add_text(self, text: str):
        self.text.append(text)

    def add_figure(self, figure: Figure):
        self.figures.append(figure)


def start_section(pdf: PDF, index: int, title: str, link: int):
        """
        Create 'chapter titles' for each section that splits the document into readable chunks
        :param ch_num: Section Number (numeral)
        :param ch_title: Section Title
        :param link: Link to allow for internal hyperlinks and interactive table of contents
        :return: None
        """
        pdf.add_page()
        # Set Link Location
        pdf.set_link(link)

        # set font
        pdf.set_font('helvetica', '', 12)
        pdf.set_fill_color(200, 220, 255)

        # Chapter Title
        pdf.cell(0, 5, f'Section {index} : {title}', ln=1, fill=1)
        # Line Break
        pdf.ln()

def write_sections(pdf: PDF, section_list: List[Section]):
    # Write table of contents
    pdf.set_font('times', '', 16)
    pdf.cell(0, 10, 'Table of Contents', ln=1)
    pdf.set_font('helvetica', '', 12)

    pdf_links = {}
    for i, section in enumerate(section_list): 
        section_link = pdf.add_link()
        pdf_links[section] = section_link
        
        pdf.cell(0, 10, f'Section {i} : {section.title}', ln=1, link=section_link)

    # Write Sections
    for i, section in enumerate(section_list):
        # Write section title
        start_section(pdf, i, section.title, pdf_links[section])
        # pdf.chapter_body(name, figure)

        # Set font
        pdf.set_font('times', '', 12)
        for line in section.text:
            pdf.cell(0, 5, line, border=1)
            pdf.ln()
       
        for figure in section.figures:
            # TODO move to figure
            fig_w, fig_h = Image.open(figure.filepath).size
            aspect_ratio = float(fig_w) / float(fig_h)
            fig_w = 90
            fig_h = fig_w / aspect_ratio

            if pdf.h - pdf.b_margin < pdf.y + fig_h:
                pdf.add_page()
                x = pdf.l_margin
                y = pdf.y + 5

            # Initially format a single Plot
            print("Left margin", pdf.l_margin)
            print("Right margin", pdf.r_margin)
            print("Fig_w", fig_w)
            pdf.image(str(figure.filepath), x=pdf.l_margin + ((pdf.w - pdf.r_margin - pdf.l_margin) / 2) - (fig_w / 2), y=pdf.y + 10, w=fig_w)
            pdf.set_y(pdf.y + 10 + fig_h + 5)
            # self.image(r"plots/User_Type_Histogram.png", x=self.w / 2, y=60, w=self.w / 2.5)
            
            text = 'Test Adding Additional Text. This graphic provides information about the distribution of visitor types within the maker space'
            pdf.multi_cell(0, 5, text)

        # Undo margin change


class ReportService():
    def __init__(self, figure_service: FigureService):
        self.figure_service = figure_service

    def generate_kpi_report(self):

        # create FPDF object
        # Layout ('P','L'); Unit ('mm', 'cm', 'in'); Format ('A3', 'A4' (default), 'A5', 'Letter', (100,150))
        pdf = PDF('P', 'mm', 'Letter')
        pdf.set_title(title)
        pdf.set_author('Anthony Riesen')

        pdf.alias_nb_pages() # sets {nb} as page number alias

        # # Links
        website = 'https://www.niacc.edu'
        # ch1_link = pdf.add_link()
        # ch2_link = pdf.add_link()
        #
        # # Get total page numbers
        #
        # # Set auto page break
        pdf.set_auto_page_break(auto=True, margin=15)
        #
        # # Add a page
        pdf.add_page()
        pdf.image('resources/Business Square.png', x=-1, w=pdf.w + 2)
        pdf.cell(0, 10, f'Report Generated on {dt.date.today()}', ln=1, align='C')  # ToDo - Format so that it adds the date created
        
        user_stats_section = Section("User Statistics")
        user_stats_section.add_text(f"Total number of users: {self.figure_service.fetch_total_number_of_users()}")
        user_stats_section.add_text(f"Average number of visits per user: {self.figure_service.fetch_average_number_of_visits_per_user()}")
        user_stats_section.add_figure(self.figure_service.create_user_type_pie_chart())
        
        visit_stats_section = Section("Visit Statistics")
        visit_stats_section.add_text("Total number of visits: 15")
        visit_stats_section.add_text("Average number of visits per user: 5")
        visit_stats_section.add_figure(self.figure_service.group_by_user_type_over_time())
        visit_stats_section.add_figure(self.figure_service.create_visit_heat_map())

        write_sections(pdf, [user_stats_section, visit_stats_section])

        pdf.output('exported_reports/Workspace Report.pdf')  # ToDo - Format so that the filename includes date created
