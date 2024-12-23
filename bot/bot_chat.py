import os

from cozepy import Coze, TokenAuth, Message, COZE_CN_BASE_URL


def start_chat_with_bot(user_message):
    """
    This function initiates a chat with the specified bot and handles the streaming chat events.
    
    Parameters:
    - 需配置到环境变量中
    - coze_api_token: The Coze API access token.
    - coze_api_base: The Coze API base URL (e.g., for different regions).
    - bot_id: The ID of the bot to interact with.
    - user_id: The user ID for identifying the user.
    - user_message: The message to send to the bot.
    """
    coze_api_token = os.getenv("COZE_API_TOKEN") or ""
    coze_api_base = os.getenv("COZE_API_BASE") or COZE_CN_BASE_URL
    bot_id = os.getenv("COZE_BOT_ID") or "7446395247313436681"
    user_id = "123"  # You can replace this with a custom user ID


    # Initialize the Coze client with the provided token and base URL
    coze = Coze(auth=TokenAuth(coze_api_token), base_url=coze_api_base)

    # Start the chat stream and process the chat events
    # for event in coze.chat.create_and_poll(
    #         bot_id=bot_id,
    #         user_id=user_id,
    #         additional_messages=[Message.build_user_question_text(user_message)],
    # ):
    #     if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
    #         # Print the message content as it arrives
    #         print(event.message.content, end="", flush=True)
    #         cosy_voice.voice_conversion.text_to_voice(event.message.content,"sk-317e606749294e5994cb605f07436c73")
    #
    #     if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
    #         # When the conversation is completed, print token usage
    #         print()
    #         print("Token usage:", event.chat.usage.token_count)

    chat_poll = coze.chat.create_and_poll(
        # id of bot
        bot_id=bot_id,
        # id of user, Note: The user_id here is specified by the developer, for example, it can be the
        # business id in the developer system, and does not include the internal attributes of coze.
        user_id=user_id,
        # user input
        additional_messages=[Message.build_user_question_text(user_message)]
    )
    if chat_poll.messages:
        return chat_poll.messages[0].content
    return None

    # for message in chat_poll.messages:
    #     print(message.content, end="")
    #
    # if chat_poll.chat.status == ChatStatus.COMPLETED:
    #     print()




# Example usage of the function:
if __name__ == "__main__":
    user_message = "给我讲一个刺激的恐怖故事"
    # Call the method to start the chat with the bot
    start_chat_with_bot( user_message)
