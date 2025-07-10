import os

def get_files_info(working_directory, directory="."):

    if directory == ".":
        print("Result for current directory:")
    else:
        print(f"Result for '{directory}' directory:")

    full_path = os.path.join(working_directory, directory)

    abs_path = os.path.abspath(full_path)
    abs_working_directory_path =  os.path.abspath(working_directory)

    if not abs_path.startswith(abs_working_directory_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'
    
    contents = ""
    items_in_dir = os.listdir(full_path)

    for item in items_in_dir:
        item_path = os.path.join(full_path, item)

        if not os.path.isfile(item_path) and not os.path.isdir(item_path):
            return f'Error: {item} is not file or dir'

        item_content = f" - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
        contents += item_content + "\n"



    return contents