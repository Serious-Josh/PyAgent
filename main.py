import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("GEMINI API_KEY NOT FOUND")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    
    for _ in range(20):
        response = client.models.generate_content(model='gemini-2.5-flash',
                                                contents=messages,
                                                config=types.GenerateContentConfig(tools=[available_functions],
                                                                                    system_instruction=SYSTEM_PROMPT,
                                                                                    temperature=0))
        
        if response.usage_metadata == None:
            raise RuntimeError("No response given. Failed API request.")
        
        # adding candidates content to messages list
        if response.candidates:
            for can in response.candidates:
                messages.append(can.content) # type: ignore

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls:
            results = []
            for call in response.function_calls:
                result = call_function(call, args.verbose)

                if not result.parts:
                    raise Exception("Error: no parts returned on call_function")
                if result.parts[0].function_response == None:
                    raise Exception("Error: call_function response is None rather than FunctionResponse")
                if result.parts[0].function_response.response == None:
                    raise Exception("Error: Call function provided no response")
                
                results.append(result.parts[0])

                if args.verbose:
                    print(f"-> {result.parts[0].function_response.response}")

            # adding function_call responses to messages list
            messages.append(types.Content(role="user", parts=results))
        else:
            print(response.text)
            return 0

    print("Problem not solved within specified iterations")
    exit(1)
if __name__ == "__main__":
    main()
