import os
import time
from venv import logger

from bot.bot_chat import start_chat_with_bot
from cosy_voice.voice_conversion import text_to_voice


def voice_cache(user_message):
    # 将长文本进行切割并转换音频
    text = start_chat_with_bot(user_message)
    to_transform_voice_list = text.split("。")

    base_path = "D:/voice_cache/"
    os.makedirs(base_path, exist_ok=True)

    store_pkg_serial_num = 0
    while True:
        store_pkg_path = base_path + str(store_pkg_serial_num) + "/"
        if not os.path.exists(store_pkg_path):
            # 如果路径不存在，则创建它
            os.makedirs(store_pkg_path, exist_ok=True)
            print(f"路径 {store_pkg_path} 已创建")
            for index, item in enumerate(to_transform_voice_list):
                output_file = store_pkg_path + str(index) + ".mp3"
                text_to_voice(item, output_file)
                print(f"已生成音频文件：{output_file}")

            logger.info("音频已创建成功,文件生成路径:",{store_pkg_path})
            break

        else:
            store_pkg_serial_num += 1
            continue

        time.sleep(1)


if __name__ == "__main__":
    # 将your-dashscope-api-key替换成您自己的API-KEY
    text_to_convert = "帮我讲一个简短点的鬼故事"
    voice_cache(text_to_convert)
