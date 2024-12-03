
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer


def text_to_voice(text, api_key, model="cosyvoice-v1", voice="longxiaochun", output_file="output.mp3"):
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
    dashscope.api_key = api_key

    synthesizer = SpeechSynthesizer(model=model, voice=voice)
    audio = synthesizer.call(text)

    request_id = synthesizer.get_last_request_id()

    with open(output_file, 'wb') as f:
        f.write(audio)

    return request_id

if __name__ == "__main__":
    # 将your-dashscope-api-key替换成您自己的API-KEY
    api_key = ""
    text_to_convert = "今天天气怎么样呀？"
    request_id = text_to_voice(text_to_convert, api_key)
    print(f"语音合成请求ID: {request_id}")