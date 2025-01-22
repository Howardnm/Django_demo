import requests


def send():
    """ 《企业微信》生产机台报修群 """
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=440cd1a6-c786-40b9-ae3a-14cc1fbac7eb"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": "test"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    records = response.json()
    return records


if __name__ == '__main__':
    send()
