from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
from google.genai import types

def call_function(function_call_part, verbose=False):

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")


    if function_call_part.name == "get_files_info":
        function_result = get_files_info("./calculator", **function_call_part.args)
    elif function_call_part.name == "get_file_content":
        function_result = get_file_content("./calculator", **function_call_part.args)
    elif function_call_part.name == "run_python_file":
        function_result = run_python_file("./calculator", **function_call_part.args)
    elif function_call_part.name == "write_file":
        function_result = write_file("./calculator", **function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

