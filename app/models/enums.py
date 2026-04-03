import enum

class ProjectRole(str, enum.Enum):
    PM = "Project Manager"
    DESIGNER = "Designer"
    FE = "Frontend Developer"
    BE = "Backend Developer"
    DEVOPS = "DevOps"
    QA = "QA"

class TaskStatus(str, enum.Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    IN_REVIEW = "In Review"
    DONE = "Done"

class TaskPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class TaskType(str, enum.Enum):
    BUG = "Bug"
    STORY = "Story"
    TASK = "Task"
    EPIC = "Epic"
    SUBTASK = "Subtask"