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
    CATEGORY = "RequestsPoster"

    def run(self, text_url, text_key, text_value):
        url = text_url
        data = {text_key: text_value}
        response = requests.post(url, data=data)

        print(response.status_code)
        print(response.text)
        return (response.text)

NODE_CLASS_MAPPINGS = {
    "TextSend": TextSend,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextSend": "TextSend",
}