import asyncio

from rich.console import Console

from .._openai import get_aoai_async_client

console = Console()

async def main() -> None:

    client = get_aoai_async_client()

    assistants = []
    async for assistant in client.beta.assistants.list():
        assistants.append(assistant)
        console.print(f'assistant: {assistant.name} ({assistant.id})')

    for assistant in assistants:
        console.print(f'deleting assistant: {assistant.name} ({assistant.id})...')
        await client.beta.assistants.delete(assistant.id)

if __name__ == '__main__':
    asyncio.run(main())