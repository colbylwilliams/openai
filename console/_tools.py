import json

from typing import Iterable

from _openai import FunctionTool
from _utils import get_json_from_file
from openai.types.beta import FunctionToolParam
from openai.types.beta.threads.required_action_function_tool_call import RequiredActionFunctionToolCall
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput

find_entities_by_kind: FunctionToolParam = {
    'type': 'function',
    'function': {
        'name': 'find_entities_by_kind',
        'description': 'Find entities of a specific kind that match a user query.',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'The text from the user, in natural language, to consider when searching for relevant entities.'
                },
                'kind': {
                    'type': 'string',
                    'description': 'The kind of entity to search for. Some examples of entity kinds include: API, template, repository, environment, operation, project, service, resource, tool, work station, PC.'
                }
            },
            'required': ['query', 'kind'],
            'additionalProperties': False
        }
    }
}

def handle_find_entities_by_kind(tool: RequiredActionFunctionToolCall) -> ToolOutput:
    arguments = json.loads(tool.function.arguments)
    query = arguments['query']
    kind = arguments['kind']

    entities = get_json_from_file(filename='entities.json')
    entities_of_kind = [entity for entity in entities if entity['kind'].lower() == kind.lower()]
    output = json.dumps(entities_of_kind)
    return ToolOutput(output=output, tool_call_id=tool.id)

find_entities_of_kinds: FunctionToolParam = {
    'type': 'function',
    'function': {
        'name': 'find_entities_of_kinds',
        'description': 'Find entities that match a specific set of kinds and match the users query.',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {
                    'type': 'string',
                    'description': 'The text from the user, in natural language, to consider when searching for relevant entities.'
                },
                'kinds': {
                    'type': 'array',
                    'items': {
                        'type': 'string'
                    },
                    'description': 'The kinds of entities to search for. Some examples of entity kinds include: API, template, repository, environment, operation, project, service, resource, tool, work station, PC.'
                }
            },
            'required': ['query', 'kinds'],
            'additionalProperties': False
        }
    }
}

def handle_find_entities_of_kinds(tool: RequiredActionFunctionToolCall) -> ToolOutput:
    arguments = json.loads(tool.function.arguments)
    query = arguments['query']
    kinds = arguments['kinds']

    entities = get_json_from_file(filename='entities.json')
    entities_of_kinds = [entity for entity in entities if entity['kind'].lower() in kinds]
    output = json.dumps(entities_of_kinds)

    return ToolOutput(output=output, tool_call_id=tool.id)

get_all_entities_of_kind: FunctionToolParam = {
    'type': 'function',
    'function': {
        'name': 'get_all_entities_of_kind',
        'description': 'Get all entities of a specific kind.',
        'parameters': {
            'type': 'object',
            'properties': {
                'kind': {
                    'type': 'string',
                    'description': 'The kind of entity to search for. Some examples of entity kinds include: API, template, repository, environment, operation, project, service, resource, tool, work station, PC.'
                }
            },
            'required': ['kind'],
            'additionalProperties': False
        }
    }
}

def handle_get_all_entities_of_kind(tool: RequiredActionFunctionToolCall) -> ToolOutput:
    arguments = json.loads(tool.function.arguments)
    kind = arguments['kind']

    entities = get_json_from_file(filename='entities.json')
    entities_of_kind = [entity for entity in entities if entity['kind'].lower() == kind.lower()]
    output = json.dumps(entities_of_kind)

    return ToolOutput(output=output, tool_call_id=tool.id)

function_tools: Iterable[FunctionTool] = [
    FunctionTool(name='find_entities_by_kind', function=find_entities_by_kind, handler=handle_find_entities_by_kind),
    FunctionTool(name='find_entities_of_kinds', function=find_entities_of_kinds, handler=handle_find_entities_of_kinds),
    FunctionTool(name='get_all_entities_of_kind', function=get_all_entities_of_kind, handler=handle_get_all_entities_of_kind)
]