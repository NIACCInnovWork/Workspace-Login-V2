from database.initialize_database import *
from reports import ReportService, FigureService

def main():
    mydb = start_workspace_database()
    fig_srv = FigureService(mydb)
    report_srv = ReportService(fig_srv)

    # generate_total_report(mydb)
    report_srv.generate_kpi_report()

if __name__ == '__main__':
    main()
