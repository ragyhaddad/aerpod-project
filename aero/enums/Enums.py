# Author: Ragy Haddad
from enum import Enum,unique
"""
    Enumerations to signal starting and queing of jobs
"""
# Job Status Enumeration
@unique
class JobStatus(Enum):
    UNLAUNCHED = 0
    RUNNING = 1 
    COMPLETED = 2 
    FAILED = 3
    NOTFOUND = 4
    QUEUED = 5
# For a given Job are all the dependancies statisfied if any exist
@unique
class DependancyStatus(Enum):
    UNLAUNCHED = 0 # All Deps UNLAUNCHED
    RUNNING = 1 # 1 or More are running 
    COMPLETED = 2 # All are completed
    FAILED = 3 # 1 or More have failed
    INDEPENDANT = 4 # a Job that has no dependencies 
    

