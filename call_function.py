from google.genai import types

# I know wildcards are no good, but I'm importing everything so it's fine
from functions.get_files_info import *
from functions.get_file_contents import *
from functions.run_python_file import *
from functions.write_file import *

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_files_contents, schema_run_python_file, schema_write_file]
)

function_map = {
        "get_file_contents": get_file_contents,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

def call_function(function_call, verbose=False):
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    function_name = function_call.name or ""

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )