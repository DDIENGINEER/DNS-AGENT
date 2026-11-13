import json
from openai import OpenAI

from app.config import OPENAI_API_KEY, OPENAI_MODEL

from app.tools import (
    search_private_dns,
    search_public_dns,
    validate_regional_dns,
    identify_dns_hosting
)


# --------------------------------------------------
# OpenAI Client
# --------------------------------------------------

client = OpenAI(api_key=OPENAI_API_KEY)


# --------------------------------------------------
# Agent System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a DDI DNS Lookup Assistant.

Your purpose is to provide DNS intelligence using
the available DNS lookup tools.

Your responsibilities:

1. Identify private DNS records.
2. Identify public DNS records.
3. Validate DNS resolution across regions.
4. Identify DNS hosting platforms.
5. Compare DNS responses across regions.

Operating instructions:

- Understand the user's DNS request.
- Select appropriate tools based on the request.
- Execute multiple tools when required.
- Consolidate the returned information.
- Never invent DNS records or IP addresses.
- Clearly distinguish private and public DNS.
- Highlight regional resolution differences.
- Identify missing records.
- If information is unavailable, say so.
- All data comes from a mock simulation dataset.
- Do not modify DNS configurations.

Response format:

1. Hostname
2. Private DNS information
3. Public DNS information
4. Regional resolution
5. DNS hosting information
6. Observations and recommendations
"""


# --------------------------------------------------
# Tool Definitions
# --------------------------------------------------

TOOLS = [

    {
        "type": "function",
        "name": "search_private_dns",
        "description": (
            "Search private DNS records for a hostname."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "hostname": {
                    "type": "string",
                    "description": "DNS hostname to search"
                }
            },
            "required": ["hostname"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "search_public_dns",
        "description": (
            "Search public DNS records for a hostname."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "hostname": {
                    "type": "string",
                    "description": "DNS hostname to search"
                }
            },
            "required": ["hostname"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "validate_regional_dns",
        "description": (
            "Validate DNS resolution across different regions."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "hostname": {
                    "type": "string",
                    "description": "DNS hostname to validate"
                }
            },
            "required": ["hostname"],
            "additionalProperties": False
        },
        "strict": True
    },

    {
        "type": "function",
        "name": "identify_dns_hosting",
        "description": (
            "Identify the DNS zone and hosting platform."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "hostname": {
                    "type": "string",
                    "description": "DNS hostname to identify"
                }
            },
            "required": ["hostname"],
            "additionalProperties": False
        },
        "strict": True
    }

]


# --------------------------------------------------
# Python Function Mapping
# --------------------------------------------------

FUNCTIONS = {

    "search_private_dns": search_private_dns,

    "search_public_dns": search_public_dns,

    "validate_regional_dns": validate_regional_dns,

    "identify_dns_hosting": identify_dns_hosting

}


# --------------------------------------------------
# Tool Execution
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    function = FUNCTIONS.get(tool_name)

    if function is None:
        return {
            "error": f"Unknown tool: {tool_name}"
        }

    try:

        result = function(**arguments)

        return result

    except Exception as error:

        return {
            "error": str(error)
        }


# --------------------------------------------------
# Main Agent
# --------------------------------------------------

def ask_dns_agent(question):

    if not question or not question.strip():
        return "Please provide a DNS hostname or question."

    try:

        # Initial AI request
        response = client.responses.create(

            model=OPENAI_MODEL,

            instructions=SYSTEM_PROMPT,

            input=question,

            tools=TOOLS

        )

        # Prevent unlimited tool execution
        max_iterations = 8

        iteration = 0

        while iteration < max_iterations:

            iteration += 1

            # Identify function calls
            function_calls = [

                item for item in response.output

                if item.type == "function_call"

            ]

            # No more function calls
            if not function_calls:

                return response.output_text

            tool_outputs = []

            # Execute requested functions
            for call in function_calls:

                arguments = json.loads(call.arguments)

                print(f"\n[AGENT TOOL] {call.name}")

                print(f"[ARGUMENTS] {arguments}")

                result = execute_tool(
                    call.name,
                    arguments
                )

                print(f"[RESULT] {result}")

                tool_outputs.append({

                    "type": "function_call_output",

                    "call_id": call.call_id,

                    "output": json.dumps(result)

                })

            # Send tool results back to OpenAI
            response = client.responses.create(

                model=OPENAI_MODEL,

                instructions=SYSTEM_PROMPT,

                previous_response_id=response.id,

                input=tool_outputs,

                tools=TOOLS

            )

        return (
            "Agent stopped because the maximum "
            "tool execution limit was reached."
        )

    except Exception as error:

        print(f"\n[AGENT ERROR] {error}")

        return f"Unable to process DNS request: {error}"
