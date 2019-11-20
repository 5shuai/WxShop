import requests
import json


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        data = {"apikey": self.api_key,
                "mobile": mobile,
                "text": "【5istudy】您好，你的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)}
        response = requests.post(self.single_send_url, data=data)
        re_dict = json.loads(response.text)
        print(re_dict)
        return re_dict


if __name__ == '__main__':
    yun_pian = YunPian("f45f627b886fdc83b312e7a9d0c8e2af")
    yun_pian.send_sms("1234", 15618919283)
