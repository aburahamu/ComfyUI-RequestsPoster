import requests

class TextSend:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_url": ("STRING", {"forceInput": True, "default": "https://~"}),
                "text_key": ("STRING", {"forceInput": True, "default": "content"}),
                "text_value": ("STRING", {"forceInput": True, "default": "Hello, World!!"}),
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "run"
    CATEGORY = "MyCustomClient"

    def run(self, text_url, text_key, text_value):
        url = text_url  # 送信先のURL
        data = {text_key: text_value}  # 送信するデータ
        response = requests.post(url, data=data)

        print(response.status_code)  # レスポンスのステータスコードを表示
        print(response.text)  # レスポンスの内容を表示
        return (response.text)

NODE_CLASS_MAPPINGS = {
    "TextSend": TextSend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextSend": "TextSend",
}