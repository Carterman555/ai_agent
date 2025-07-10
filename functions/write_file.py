import os

def write_file(working_directory, file_path, content):

    combined_path = os.path.join(working_directory, file_path)

    abs_path = os.path.abspath(combined_path)
    abs_working_directory_path =  os.path.abspath(working_directory)

    if not abs_path.startswith(abs_working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        dir_path = os.path.dirname(combined_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception as e:
        return f'Error: Error when checking if path exists "{combined_path}": {str(e)}'

    try:
        with open(combined_path, "w") as f:
            f.write(content)
    except PermissionError:
        return f'Error: Permission denied when writing to "{file_path}"'
    except Exception as e:
        return f'Error: Could not write to "{file_path}": {str(e)}'

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


