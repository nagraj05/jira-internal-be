import enum

class ProjectRole(str, enum.Enum):
    PM = "Project Manager"
    DESIGNER = "Designer"
    FE = "Frontend Developer"
    BE = "Backend Developer"
    DEVOPS = "DevOps"
    QA = "QA"