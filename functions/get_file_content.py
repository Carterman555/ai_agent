import os
from config import FILE_CHAR_LIMIT

def get_file_content(working_directory, file_path):

    combined_path = os.path.join(working_directory, file_path)

    abs_path = os.path.abspath(combined_path)
    abs_working_directory_path =  os.path.abspath(working_directory)

    if not abs_path.startswith(abs_working_directory_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(combined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(combined_path, "r") as f:
        file_content_string = f.read(FILE_CHAR_LIMIT)

    if len(file_content_string) == FILE_CHAR_LIMIT:
        file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'

    
    return file_content_string
