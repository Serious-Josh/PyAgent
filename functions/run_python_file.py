import os, subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]

    if args:
        command.extend(args)

    try:
        process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        out_string = ''

        if process.returncode != 0:
            out_string += f"Process exited with code {process.returncode}"
        if process.stdout:
            out_string += f"STDOUT: {process.stdout}"
        if process.stderr:
            out_string += f"STDERR: {process.stderr}"
        if not out_string:
            out_string = "No output produced"
        
    except Exception as e:
        return f'Error: executing Python file: {e}'

    return out_string