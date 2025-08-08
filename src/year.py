from dataclasses import dataclass

# The dataclass that holds the given funds for each year, from year 1 and up.
@dataclass
class Year:
    allocated_funds: int

# The standard years used for the simulation.
STANDARD_YEARS = [
    Year(23), # Year 1
    Year(35), # Year 2
    Year(46), # ...
    Year(58),
    Year(58),
    Year(58),
    Year(58),
    Year(58),
    Year(58),
]
