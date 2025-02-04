import json

from common import util
from common.logger import log
from . import PushChannel


class WeComBot(PushChannel):
    def __init__(self, config):
        super().__init__(config)
        self.key = str(config.get("key", ""))
        if self.key == "":
            log.error(f"【推送_{self.name}】配置不完整，推送功能将无法正常使用")

    def push(self, title, content, jump_url=None, pic_url=None):
        push_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": self.key
        }
        body = {
            "msgtype": "news",
            "news": {
                "articles": [
                    {
                        "title": title,
                        "description": content,
                        "url": jump_url,
                    }
                ]
            }
        }

        if pic_url is not None:
            body["news"]["articles"][0]["picurl"] = pic_url

        response = util.requests_post(push_url, self.name, headers=headers, params=params, data=json.dumps(body))
        push_result = "成功" if util.check_response_is_ok(response) else "失败"
        log.info(f"【推送_{self.name}】{push_result}")
