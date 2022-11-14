from database.initialize_database import *
from reports.total_report import generate_total_report

def main():
    mydb = start_workspace_database()
    generate_total_report(mydb)

if __name__ == '__main__':
    main()
