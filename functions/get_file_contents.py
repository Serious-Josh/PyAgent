import os
from config import MAX_CHARS

def get_file_contents(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
        return f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        file = open(target_file)
        contents = file.read(10000)

        if file.read(1):
            contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"
    
    return contents