from venv import logger

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer

import nls
import time

from cosy_voice.AliyunTokenGenerator import AliyunTokenGenerator

# 设置打开日志输出
nls.enableTrace(False)

# 将音频保存进文件
SAVE_TO_FILE = True
# 将音频通过播放器实时播放，需要具有声卡。在服务器上运行请将此开关关闭
PLAY_REALTIME_RESULT = True
if PLAY_REALTIME_RESULT:
    import pyaudio


def text_to_voice(text, output_file):
    if SAVE_TO_FILE:
        file = open(output_file, "wb")
    if PLAY_REALTIME_RESULT:
        player = pyaudio.PyAudio()
        stream = player.open(
            format=pyaudio.paInt16, channels=1, rate=24000, output=True
        )

        # 创建SDK实例
        # 配置回调函数

    def on_data(data, *args):
        if SAVE_TO_FILE:
            file.write(data)
        if PLAY_REALTIME_RESULT:
            stream.write(data)

    def on_message(message, *args):
        print("on message=>{}".format(message))

    def on_close(*args):
        print("on_close: args=>{}".format(args))

    def on_error(message, *args):
        print("on_error message=>{} args=>{}".format(message, args))

    ak = ""
    aks = ""

    # 初始化 AliyunTokenClient
    client = AliyunTokenGenerator(access_key_id=ak, access_key_secret=aks)

    # 获取 Token
    try:
        token_data = client.create_token()
        print("Token:", token_data["token"])
        print("Expire Time:", token_data["expireTime"])
    except RuntimeError as e:
        print("Error:", e)

    sdk = nls.NlsStreamInputTtsSynthesizer(
        # 由于目前阶段大模型音色只在北京地区服务可用，因此需要调整url到北京
        url="wss://nls-gateway-cn-beijing.aliyuncs.com/ws/v1",
        token=token_data["token"],
        appkey="dB2VfKnIiLeJT9j7",
        on_data=on_data,
        on_sentence_begin=on_message,
        on_sentence_synthesis=on_message,
        on_sentence_end=on_message,
        on_completed=on_message,
        on_error=on_error,
        on_close=on_close,
        callback_args=[],
    )

    # 发送文本消息
    sdk.startStreamInputTts(
        voice="longmei",  # 语音合成说话人
        aformat="wav",  # 合成音频格式
        sample_rate=24000,  # 合成音频采样率
        volume=50,  # 合成音频的音量
        speech_rate=0,  # 合成音频语速
        pitch_rate=0,  # 合成音频的音调
    )
    sdk.sendStreamInputTts(text)

    # for text in test_text:
    #     sdk.sendStreamInputTts(text)
    #     time.sleep(0.05)
    sdk.stopStreamInputTts()
    if SAVE_TO_FILE:
        file.close()
    if PLAY_REALTIME_RESULT:
        stream.stop_stream()
        stream.close()
        player.terminate()


if __name__ == "__main__":
    # 将your-dashscope-api-key替换成您自己的API-KEY
    text_to_convert = "今天天气怎么样呀？"
    request_id = text_to_voice(text_to_convert)
    print(f"语音合成请求ID: {request_id}")
