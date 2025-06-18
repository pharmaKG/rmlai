import argparse
from typing import List, Dict

import re
import json
from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel

class ListResponse(BaseModel):
    response: List[str]

class JsonResponse(BaseModel):
    response: Dict[str, str]

class StringResponse(BaseModel):
    response: str

class FloatResponse(BaseModel):
    response: float

## TODO refactor
def query_for_str(prompt) -> str:
    response: ChatResponse = chat(
        model='deepseek-r1:14b',
        messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ])
    parsed = None
    try:
        response_content = response['message']['content']
        parsed = re.search(r"</think>([\s\S]*)", response_content, flags=re.DOTALL).group(1).strip()
        data = json.loads(parsed)
        validated = StringResponse(**data)
        return validated.response
    except Exception as e:
        raise ValueError(f"Parsed output: || {parsed} || INVALID STRING output: {e}")

def query_for_list(prompt) -> List[str]:
    response: ChatResponse = chat(
        model='deepseek-r1:14b',
        messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    parsed = None
    try:
        response_content = response['message']['content']
        parsed = re.search(r"</think>([\s\S]*)", response_content, flags=re.DOTALL).group(1).strip()
        data = json.loads(parsed)
        validated = ListResponse(response=data)
        return validated.response
    except Exception as e:
        raise ValueError(f"Parsed output: || {parsed} || has INVALID LIST output: {e}")

def query_for_float(prompt) -> float:
    response: ChatResponse = chat(
        model='deepseek-r1:14b',
        messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    parsed = None
    try:
        response_content = response['message']['content']
        parsed = re.search(r"</think>([\s\S]*)", response_content, flags=re.DOTALL).group(1).strip()
        data = json.loads(parsed)
        validated = FloatResponse(**data)
        return validated.response
    except Exception as e:
        raise ValueError(f"Parsed output: || {parsed} || has INVALID FLOAT output: {e}")

def main():
    parser = argparse.ArgumentParser(description="Query OLLAMA")
    parser.add_argument("--return_type", type=str, default="str", help="Select return type. Default value str.")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt for LLM.")

    args = parser.parse_args()

    if args.return_type == "list":
        print(query_for_list(args.prompt))
    elif args.return_type == "float":
        print(query_for_float(args.prompt))
    else:
        print(query_for_str(args.prompt))


if __name__ == '__main__':
    main()