import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

if len(sys.argv) <= 1:
    raise Exception("Error: no message given!")

verbose = len(sys.argv) >= 3 and sys.argv[2] == "--verbose"

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.

1. Make a plan
2. Execute the plan
    You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
3. When completed, say "Task Complete"

"""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to get contents of, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the code of the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to execute, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites the content of the specified file. Creates a new directories and file if path or file doesn't exist",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

if verbose: 
    print(f"User prompt: {user_prompt}")

max_iterations = 20
for x in range(max_iterations):

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )
        )
    except Exception as e:
        raise Exception(f"Error: Could not generate response. Error: {e}, Messages: {messages}.")

    try:
        messages.append(response.candidates[0].content)
    except Exception as e:
        raise Exception(f"Error: failed to add model response to messages. Error: {e}. Candidates: {response.candidates}")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates[0].content.parts[0].text != None:
        print(f"Model: {response.candidates[0].content.parts[0].text}")

        if "Task Complete" in response.candidates[0].content.parts[0].text:
            break

    try:
        if response.function_calls != None:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)

                if function_call_result.parts[0].function_response.response != None:
                    function_response = function_call_result.parts[0].function_response.response["result"]
                    messages.append(types.Content(role="user", parts=[types.Part(text=function_response)]))
                    if verbose:
                        print(f"-> {function_response}")
                else:
                    raise Exception(f"Error: No function call response for {function_call.name}")
        else:
            print("Function calls is None")
    except Exception as e:
        raise Exception(f"Error: Failed to call function. Error: {e}, Function Calls: {response.function_calls}")
    