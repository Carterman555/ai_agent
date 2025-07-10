import os
import subprocess

def run_python_file(working_directory, file_path):

    combined_path = os.path.join(working_directory, file_path)

    abs_path = os.path.abspath(combined_path)
    abs_working_directory_path = os.path.abspath(working_directory)

    if not abs_path.startswith(abs_working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(combined_path):
        return f'Error: File "{file_path}" not found.'

    extension = file_path.split(".")[1]
    if extension != "py":
        return f'Error: "{file_path}" with extension "{extension}" is not a Python file.'

    try:
        process = subprocess.run(["python3", combined_path], capture_output=True, timeout=30)
    except Exception as e:
        return f"Error: executing Python file - path: {combined_path}, error: {e}"

    if process.stdout == None and process.stderr == None:
        return "No output produced."

    output = f"""
    STDOUT: {process.stdout}
    STDERR: {process.stderr}
    """

    if process.returncode != 0:
        output += f"Process exited with code {process.returncode}"

    return output