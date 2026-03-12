import os

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
        return f'Error: Cannot read "{target_file}" as it is outside the permitted working directory'
    
    if os.path.isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    # Ensure directory path exists
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    try:
        file = open(target_file, 'w')
        file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'