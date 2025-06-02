from aioinject import Injected, inject

from app.service_layer import AConversationsService


@inject
async def get_conversations_stats(conversations_service: Injected[AConversationsService]) -> None:
    page = 1
    conversations_count = 0
    while True:
        conversations = await conversations_service.search(page, per_page=10)
        page += 1
        if not conversations:
            break
        conversations_count += len(conversations)
    print(f"Conversations exist at the moment: {conversations_count}")
