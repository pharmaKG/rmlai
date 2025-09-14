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

##TODO: refactor
def query_for_str(prompt, model) -> str:
    response = query(prompt, model)
    parsed = None
    try:
        response_content = response['message']['content']
        parsed = re.search(r"</think>([\s\S]*)", response_content, flags=re.DOTALL).group(1).strip()
        data = json.loads(parsed)
        validated = StringResponse(**data)
        return validated.response
    except Exception as e:
        raise ValueError("Parsed output: || {} || INVALID STRING output: {}".format(parsed, e))


def query(prompt, model="deepseek-r1:14b", temperature=0) -> ChatResponse:
    response = chat(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': prompt,
            },
        ],
        options={
            'temperature': temperature
        }
    )

    return response

def query_with_chaining(messages, model="deepseek-r1:14b", temperature=0) -> ChatResponse:
    response = chat(
        model=model,
        messages=messages,
        options={
            'temperature': temperature
        }
    )

    return response

def query_for_list(prompt, model) -> List[str]:
    response = query(prompt, model)
    parsed = None
    try:
        response_content = response['message']['content']
        parsed = re.search(r"</think>([\s\S]*)", response_content, flags=re.DOTALL).group(1).strip()
        data = json.loads(parsed)
        validated = ListResponse(response=data)
        return validated.response
    except Exception as e:
        raise ValueError("Parsed output: || {} || has INVALID LIST output: {}".format(parsed, e))

def query_for_float(prompt, model) -> float:
    response = query(prompt, model)
    parsed = None
    try:
        response_content = response['message']['content']
        parsed = re.search(r"</think>([\s\S]*)", response_content, flags=re.DOTALL).group(1).strip()
        data = json.loads(parsed)
        validated = FloatResponse(**data)
        return validated.response
    except Exception as e:
        raise ValueError("Parsed output: || {} || has INVALID FLOAT output: {}".format(parsed, e))

def query_general(prompt, model, temperature=0) -> str:
    response = query(prompt, model, temperature)
    response_content = response['message']['content']
    return response_content

def clean_query_general(prompt, model, temperature=0) -> str:
    response = query(prompt, model, temperature)
    response_content = response['message']['content']
    match = re.search(r"</think>([\s\S]*)", response_content, flags=re.DOTALL)
    return match.group(1).strip() if match else ""

def query_general_with_chaining(messages, model, temperature=0) -> str:
    response = query_with_chaining(messages, model, temperature)
    response_content = response['message']['content']
    return response_content

def main():
    parser = argparse.ArgumentParser(description="Query OLLAMA")
    parser.add_argument("--return_type", type=str, help="Select return type.")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt for LLM.")
    parser.add_argument("--model", type=str, default="deepseek-r1:14b", help="LLM model to call. Default is deepseek-r1:14b.")

    args = parser.parse_args()

    if args.return_type == "list":
        print(query_for_list(args.prompt, args.model))
    elif args.return_type == "float":
        print(query_for_float(args.prompt, args.model))
    elif args.return_type == "str":
        print(query_for_str(args.prompt, args.model))
    else:
        print(query_general(args.prompt, args.model))


if __name__ == '__main__':
    main()