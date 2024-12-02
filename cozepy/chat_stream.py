import os

from cozepy import Coze, TokenAuth, Message, ChatEventType, COZE_CN_BASE_URL


def start_chat_with_bot(coze_api_token, coze_api_base, bot_id, user_id, user_message):
    """
    This function initiates a chat with the specified bot and handles the streaming chat events.
    
    Parameters:
    - coze_api_token: The Coze API access token.
    - coze_api_base: The Coze API base URL (e.g., for different regions).
    - bot_id: The ID of the bot to interact with.
    - user_id: The user ID for identifying the user.
    - user_message: The message to send to the bot.
    """
    # Initialize the Coze client with the provided token and base URL
    coze = Coze(auth=TokenAuth(coze_api_token), base_url=coze_api_base)

    # Start the chat stream and process the chat events
    for event in coze.chat.stream(
            bot_id=bot_id,
            user_id=user_id,
            additional_messages=[Message.build_user_question_text(user_message)],
    ):
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            # Print the message content as it arrives
            print(event.message.content, end="", flush=True)

        if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
            # When the conversation is completed, print token usage
            print()
            print("Token usage:", event.chat.usage.token_count)


# Example usage of the function:
if __name__ == "__main__":
    # Get access token and base URL from environment variables
    # coze_api_token = os.getenv("COZE_API_TOKEN")
    coze_api_token = ""
    coze_api_base = os.getenv("COZE_API_BASE") or COZE_CN_BASE_URL

    # Bot and user information (replace with actual values)
    bot_id = os.getenv("COZE_BOT_ID") or ""
    user_id = "123"  # You can replace this with a custom user ID
    user_message = "讲个故事吧"

    # Call the method to start the chat with the bot
    start_chat_with_bot(coze_api_token, coze_api_base, bot_id, user_id, user_message)
