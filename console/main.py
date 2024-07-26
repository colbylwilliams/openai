import asyncio
import os

from typing import List

from _openai import FunctionTool, call_function_tool, create_assistant_async, get_aoai_async_client
from _tools import function_tools as entity_function_tools
from _utils import status
from openai.types.beta import AssistantStreamEvent
from openai.types.beta.threads import Text, TextDelta
from openai.types.beta.threads.run_submit_tool_outputs_params import ToolOutput
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
from rich.text import Text
from typing_extensions import override

from openai import AsyncAssistantEventHandler, AsyncAzureOpenAI


class AsyncEventHandler(AsyncAssistantEventHandler):

    def __init__(self, client: AsyncAzureOpenAI, function_tools: List[FunctionTool],
                 console: Console, live: Live, response: str = '') -> None:
        super().__init__()
        self.client = client
        self.function_tools = function_tools
        self.console = console
        self.live = live
        self.response = response

    @override
    async def on_event(self, event: AssistantStreamEvent) -> None:
        if event.event == 'thread.run.requires_action' and event.data.required_action.type == 'submit_tool_outputs':

            tool_outputs: List[ToolOutput] = []

            for tool in event.data.required_action.submit_tool_outputs.tool_calls:

                self.console.print(f'>> called tool function: {tool.function.name} with arguments: {tool.function.arguments}', style='dim')
                output = call_function_tool(tool, self.function_tools)
                tool_outputs.append(output)

            self.live.update(status('assistant is responding (submitting tool outputs)...'))

            async with self.client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=AsyncEventHandler(client=self.client, function_tools=self.function_tools,
                                                console=self.console, live=self.live, response=self.response),
            ) as stream:
                await stream.until_done()

    @override
    async def on_text_created(self, text: Text) -> None:
        self.console.line()

    @override
    async def on_text_delta(self, delta: TextDelta, snapshot: Text) -> None:
        self.response += delta.value
        self.live.update(Markdown(self.response), refresh=True)

async def main() -> None:

    console = Console()

    with Live(console=console, refresh_per_second=12.5, transient=True) as live:

        live.update(status('creating open ai client...'))
        client= get_aoai_async_client()

        if assistant_id := os.environ.get('OPENAI_ASSISTANT_ID'):
            live.update(status(f'retrieving assistant ({assistant_id})...'))
            assistant = await client.beta.assistants.retrieve(assistant_id)
        else: # create a new assistant if one was not provided
            live.update(status('creating assistant...'))
            assistant = await create_assistant_async(client=client, function_tools=entity_function_tools)

        live.update(status('creating thread...'))
        thread = await client.beta.threads.create()

    while True:
        console.print('\n:nerd_face: user: ', style='dim', end='')
        user_input = console.input()

        if user_input.lower() == 'exit' or user_input.lower() == 'quit' or user_input.lower() == 'q':
            console.print('\n:robot: assistant: ', style='dim', end='')
            console.print('ok, see ya :wave:')

            if assistant_id is None: # delete the assistant if it was created in this session
                with Live(console=console, refresh_per_second=12.5, transient=True) as live:

                    live.update(status('deleting assistant...'))
                    await client.beta.assistants.delete(assistant.id)

            console.line()
            break

        console.print('\n:robot: assistant', style='dim')

        with Live(console=console, refresh_per_second=12.5) as live:

            live.update(status('sending message...'))
            await client.beta.threads.messages.create(thread_id=thread.id, content=user_input, role='user')

            live.update(status('creating run...'))
            async with client.beta.threads.runs.stream(
                thread_id = thread.id,
                assistant_id = assistant.id,
                event_handler = AsyncEventHandler(client=client, function_tools=entity_function_tools, console=console, live=live),
            ) as stream:
                live.update(status('assistant is responding...'))
                await stream.until_done()

if __name__ == '__main__':
    asyncio.run(main())