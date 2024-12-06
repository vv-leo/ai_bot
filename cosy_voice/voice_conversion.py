from venv import logger

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer


def text_to_voice(text, output_file):
    """
    将输入的文本转换为MP3音频文件。

    Args:
        text (str): 要转换为音频的文本内容。
        api_key (str): DashScope的API密钥。
        model (str, optional): 使用的语音合成模型，默认为"cosyvoice-v1"。
        voice (str, optional): 语音类型，默认为"longxiaochun"。
        output_file (str, optional): 输出的MP3文件路径，默认为"output.mp3"。

    Returns:
        str: 本次语音合成的请求ID。
    """

    model = "cosyvoice-v1"
    voice = "longxiaochun"
    api_key = ""
    dashscope.api_key = api_key

    synthesizer = SpeechSynthesizer(model=model, voice=voice)

    try:
        # 调用语音合成API
        print("text----->voice:", text)
        if not text or not text.strip():
            return

        audio = synthesizer.call(text)
        # 将音频数据写入文件
        with open(output_file, 'wb') as f:
            f.write(audio)
        # logger.info('requestId: ', synthesizer.get_last_request_id())
    except Exception as e:
        logger.error(f"语音合成失败, 错误信息: {e}")

        # TODO 作为数据的回滚机制 ***
        # 处理错误:后续添加故事包文件回滚机制,如果一个文件发生转换异常,为了保持文件数据的完整性
        # 删除当前文件夹


if __name__ == "__main__":
    # 将your-dashscope-api-key替换成您自己的API-KEY
    text_to_convert = "今天天气怎么样呀？"
    request_id = text_to_voice(text_to_convert)
    print(f"语音合成请求ID: {request_id}")
