import requests

class RequestSettings:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_url": ("STRING", {"multiline": False}),
                "text_key": ("STRING", {"multiline": False}),
                "text_value": ("STRING", {"multiline": False})
            }
        }
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    FUNCTION = "run"
    CATEGORY = "RequestSettings"

    def run(self, text_url, text_key, text_value):
        return (text_url, text_key, text_value)

class PostRequests:
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
    "RequestSettings": RequestSettings,
    "PostRequests": PostRequests,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RequestSettings": "RequestSettings",
    "PostRequests": "PostRequests",
}