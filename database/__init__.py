"""
Provides a collection of domain objects and corresponding repositories for storing objects in the database.

Domain Objects
--------------

The object domain resembles the following. Note that this excludes join tables and other details which are specific for
db implementation. This is specifically focused on the domain model itself.

```mermaid
erDiagram
    USER ||..|{ VISIT : performs
    EQUIPMENT }|--|{ MATERIAL : "Can consume"
    CONSUMED_MATERIAL ||--|| MATERIAL : "of type"

    WORKLOG ||--|{ VISIT : "worked on"
    WORKLOG ||--|{ PROJECT : "on project"
    WORKLOG }|--|{ CONSUMED_MATERIAL : "logs"
    WORKLOG }|--|{ EQUIPTMENT_USAGE : "logs"
    EQUIPTMENT_USAGE }|--|{ EQUIPTMENT : "of type"
```

The aggregates (IE thigs you can pull out of a database) are:
* User
* Visit (WorkLog(MaterialUsage, EquipmentUsage, MaterialUsage))
* Project
* Equiptment (Material)


Repository Objects
------------------
There is, in general, one repository object per aggregate object.  General usage and particularly when mutating and 
adding data, the application should ALWAYS follow the object graph.

Some querying situations may require querying accross a few relationships. These queries should be exclusivly handled 
by the repository.  Once the domain objects are in memory, they should continue to be operated on by following the 
domain model. Some examples of these implementats would be:

* Fetch all projects on which a user worked
* Fetch all Projects in which a particular pice of equiptment was used
"""

# Models
from database.class_user import User, UserType
from database.class_project import Project, ProjectType 
from database.class_visit import Visit

# Repositories
from database.class_user import UserRepository
from database.class_project import ProjectRepository
from database.class_visit import VisitRepository
