"""
NIACC Innovation Workspace Login V2
This file defines the controller that creates a new user by receiving data from the user interface and pushing it
to the database.
Author: Anthony Riesen
"""
import tkinter.messagebox

from database import User, UserType, UserRepository, Visit, VisitRepository
from database.initialize_database import start_workspace_database


def create_user_from_ui(name: str, user_type: str):
    """
    Takes data from the UI, checks whether a member already exists in the database, if it does, displays a message,
    if it does not, calls the function to add the user to the database.
    :param name: User's name input from UI
    :param user_type: User type, input from UI, ENUM which can be 1 - 5
    :return: none
    """
    database = start_workspace_database()
    user_repo = UserRepository(database)
    visit_repo = VisitRepository(database)
    print(name, user_type)

    try:
        user = user_repo.load_by_name(name)  # If the name doesn't have to be unique, this could be eliminated
        # user = User.load(database, user_id)
    except TypeError:
        user = user_repo.create(name, UserType[user_type])
        visit = visit_repo.create_for(user)
        tkinter.messagebox.showinfo("Member Created!",
                                    "Your new member has been created and you've been logged in for your first visit!")
    else:
        print("This member already exists.")
        tkinter.messagebox.showwarning("Member Already Exists!",
                                       "The User Name you have entered already exists. \n\n"
                                       "If you have already created a user, choose 'Log In' instead. \n\n"
                                       "If you need to create new user, please try again and choose a unique name.  "
                                       "Consider using a middle initial or using a nickname instead.")
