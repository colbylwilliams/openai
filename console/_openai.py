import os

from typing import Callable, List, NamedTuple

from _utils import get_text
from azure.identity import AzureCliCredential, get_bearer_token_provider
from azure.identity.aio import AzureCliCredential as AsyncAzureCliCredential
from azure.identity.aio import get_bearer_token_provider as get_bearer_token_provider_async
from dotenv import load_dotenv
from openai.lib.azure import AsyncAzureADTokenProvider, AzureADTokenProvider
from openai.types.beta import Assistant, FunctionToolParam
from openai.types.beta.threads.required_action_function_tool_call import RequiredActionFunctionToolCall
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput

from openai import AsyncAzureOpenAI, AzureOpenAI


class FunctionTool(NamedTuple):
    name: str
    function: FunctionToolParam
    handler: Callable[[RequiredActionFunctionToolCall], ToolOutput | None]

def _get_gpt_model() -> str:
    if model := os.environ.get('OPENAI_ASSISTANT_MODEL'):
        return model
    raise ValueError(f"No GPT model found. Please set the 'OPENAI_ASSISTANT_MODEL' environment variable.")

def _get_aad_token_provider() -> AzureADTokenProvider:
    if tenant_id := os.environ.get('AZURE_TENANT_ID'):
        credential = AzureCliCredential(tenant_id=tenant_id)
        return get_bearer_token_provider(credential, 'https://cognitiveservices.azure.com/.default')
    return None

def _get_aad_token_provider_async() -> AsyncAzureADTokenProvider:
    if tenant_id := os.environ.get('AZURE_TENANT_ID'):
        credential = AsyncAzureCliCredential(tenant_id=tenant_id)
        return get_bearer_token_provider_async(credential, 'https://cognitiveservices.azure.com/.default')
    return None

def get_aoai_client() -> AzureOpenAI:
    '''Get an Azure OpenAI client using environment variables.'''
    # Load environment variables from the .env file
    load_dotenv(override=True)

    # AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION are automatically inferred from the environment variables
    if os.environ.get('AZURE_OPENAI_API_KEY'):
        return AzureOpenAI()
    elif aad_token_provider := _get_aad_token_provider():
        return AzureOpenAI(azure_ad_token_provider=aad_token_provider)
    else:
        raise ValueError(f"No authentication method found. Please set the 'AZURE_OPENAI_API_KEY' or 'AZURE_TENANT_ID' environment variable.")

def get_aoai_async_client() -> AsyncAzureOpenAI:
    '''Get an Async Azure OpenAI client using environment variables.'''
    # Load environment variables from the .env file
    load_dotenv(override=True)

    # AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, OPENAI_API_VERSION are automatically inferred from the environment variables
    if os.getenv('AZURE_OPENAI_API_KEY'):
        return AsyncAzureOpenAI()
    elif aad_token_provider := _get_aad_token_provider_async():
        return AsyncAzureOpenAI(azure_ad_token_provider=aad_token_provider)
    else:
        raise ValueError(f"No authentication method found. Please set the 'AZURE_OPENAI_API_KEY' or 'AZURE_TENANT_ID' environment variable.")

def create_assistant(client: AzureOpenAI, function_tools: List[FunctionTool]) -> Assistant:
    '''Create a new assistant using environment variables with the provided function tools.'''
    model = _get_gpt_model()
    return client.beta.assistants.create(
        name=os.environ.get('OPENAI_ASSISTANT_NAME', 'Helpful Assistant'),
        description=os.environ.get('OPENAI_ASSISTANT_DESCRIPTION', 'A helpful assistant.'),
        instructions=get_text(filename=os.environ.get('OPENAI_ASSISTANT_INSTRUCTIONS_FILE', 'instructions.sample.txt')),
        model=model,
        tools=[tool.function for tool in function_tools],
    )

async def create_assistant_async(client: AsyncAzureOpenAI, function_tools: List[FunctionTool]) -> Assistant:
    '''Create a new assistant using environment variables with the provided function tools.'''
    model = _get_gpt_model()
    return await client.beta.assistants.create(
        name=os.environ.get('OPENAI_ASSISTANT_NAME', 'Helpful Assistant'),
        description=os.environ.get('OPENAI_ASSISTANT_DESCRIPTION', 'A helpful assistant.'),
        instructions=get_text(filename=os.environ.get('OPENAI_ASSISTANT_INSTRUCTIONS_FILE', 'instructions.sample.txt')),
        model=model,
        tools=[tool.function for tool in function_tools],
    )

def call_function_tool(tool: RequiredActionFunctionToolCall, function_tools: List[FunctionTool]) -> ToolOutput:
    '''Call the appropriate function tool handler based on the tool's function name.'''
    for function_tool in function_tools:
        if tool.function.name == function_tool.name:
            return function_tool.handler(tool)
    raise ValueError(f"Unsupported function call provided '{tool.function.name}'.")