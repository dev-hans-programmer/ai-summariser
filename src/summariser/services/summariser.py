from openai import AsyncOpenAI


async def summarise_ticket(ticket: str, client: AsyncOpenAI):

    response = await client.responses.create(
        model="gpt-5.6-luna",
        input=f"Summarize this support ticket in 2 lines : \n\n{ticket}",
    )
    return response.output_text
