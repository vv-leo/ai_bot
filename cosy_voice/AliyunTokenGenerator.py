#! /usr/bin/env python
# coding=utf-8
import os
import time
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

class AliyunTokenGenerator:
    def __init__(self, access_key_id, access_key_secret, region="cn-shanghai"):
        """
        初始化阿里云Token生成器。

        :param access_key_id: 阿里云Access Key ID
        :param access_key_secret: 阿里云Access Key Secret
        :param region: 阿里云服务区域，默认"cn-shanghai"
        """
        self.client = AcsClient(access_key_id, access_key_secret, region)

    def create_token(self):
        """
        调用阿里云CreateToken API生成Token。

        :return: 返回包含token和过期时间的字典，格式为{"token": token_id, "expireTime": expire_time}。
        """
        request = CommonRequest()
        request.set_method('POST')
        request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
        request.set_version('2019-02-28')
        request.set_action_name('CreateToken')

        try:
            response = self.client.do_action_with_exception(request)
            response_data = json.loads(response)

            if 'Token' in response_data and 'Id' in response_data['Token']:
                token = response_data['Token']['Id']
                expire_time = response_data['Token']['ExpireTime']
                return {"token": token, "expireTime": expire_time}
            else:
                raise ValueError("Invalid response format: 'Token' or 'Id' is missing.")

        except Exception as e:
            print(f"Error occurred while creating token: {e}")
            return None