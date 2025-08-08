from pathlib import Path

import pandas as pd
from pandas import Series

from src.data import SimulationResult
from src.project import Project, SubProject

from config import PROJECTS_SHEET_NAME


def load_projects_from_file(file_path: Path) -> list[Project]:
    """
    This function dynamically reads all projects from a sheet named as per the config,
    and converts each row into a Project object.

    param file_path: the path to the excel file storing the projects.
    return: loaded projects.

    """
    projects = []

    MIN_PROJECTS = 1
    MAX_PROJECTS = 100

    try:
        project_df = pd.read_excel(
            file_path,
            sheet_name=PROJECTS_SHEET_NAME,
            usecols="B:S",
            dtype=int,
        )
    except FileNotFoundError:
        # Re-raise the error with a more informative message.
        raise FileNotFoundError(
            f"The specified input file was not found at: {file_path}"
        )
    except ValueError as e:
        # Catch errors from pandas if the sheet doesn't exist and provide a clear message.
        if "Worksheet" in str(e) and f"named '{PROJECTS_SHEET_NAME}' not found" in str(
            e
        ):
            raise ValueError(
                f"The Excel file must contain a sheet named '{PROJECTS_SHEET_NAME}'."
            ) from e
        # Re-raise any other ValueError.
        raise e

    # Dynamically determine the number of projects and validate against config limits.
    project_count = len(project_df)

    # print("Projects found in file: "  + str(project_count))

    if not (MIN_PROJECTS <= project_count <= MAX_PROJECTS):
        raise ValueError(
            f"The number of projects in the sheet '{PROJECTS_SHEET_NAME}' must be "
            f"between {MIN_PROJECTS} and {MAX_PROJECTS}, but {project_count} were found."
        )

    # Convert each row in the DataFrame to a Project object.
    for index, row in project_df.iterrows():
        sub_projects = convert_row_to_sub_projects(row)
        projects.append(Project(0, sub_projects))

    for project in projects:
        assert len(project.sub_projects) == 6

    return projects


def save_simulation_results_to_excel(simulation_result: SimulationResult, path: Path):
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for manager_name, manager_result in simulation_result.managers.items():
            # Define the years for the x-axis
            years = [f"year_{i}" for i in range(1, 10)]

            # Extract value and cash data from each year into dictionaries
            value_data = {year: getattr(manager_result, year).value for year in years}
            cash_data = {year: getattr(manager_result, year).cash for year in years}

            # Convert the dictionaries into DataFrames, with years as columns
            value_df = pd.DataFrame(value_data)
            cash_df = pd.DataFrame(cash_data)

            # Write the DataFrames to separate sheets in the Excel file.
            # Each run creates new sheets (overwriting previous ones if the file exists)
            value_df.to_excel(
                writer, sheet_name=f"{manager_name}-value-result", index=False
            )
            cash_df.to_excel(
                writer, sheet_name=f"{manager_name}-cash-result", index=False
            )


def convert_row_to_sub_projects(df: Series) -> list[SubProject]:
    sub_projects = []

    data_list = [int(x) for x in df]

    for i in range(6):
        sunk_pos = 3 * i
        salvageable_pos = 3 * i + 1
        risk_pos = 3 * i + 2
        risk = False

        if data_list[risk_pos] != 0:
            risk = True

        sub_projects.append(
            SubProject(risk, data_list[sunk_pos], data_list[salvageable_pos])
        )

    return sub_projects
