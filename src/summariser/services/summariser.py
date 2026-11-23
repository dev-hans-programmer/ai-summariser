from openai import AsyncOpenAI

history: list[dict[str, str]] = []


async def summarise_ticket(ticket: str, client: AsyncOpenAI):

    response = await client.responses.create(
        model="gpt-5.6-luna",
        input=f"Summarize this support ticket in 2 lines : \n\n{ticket}",
    )
    return response.output_text


async def chat_with_llm(client: AsyncOpenAI, query: str):
    history.append({"role": "user", "content": query})

    response = await client.responses.create(
        model="gpt-5.6-luna", instructions="", input=history, store=False
    )
    answer = response.output_text

    history.append({"role": "assistant", "content": answer})
    return answer
