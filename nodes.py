import requests

class PostRequests:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_url": ("STRING", {"multiline": False, "default": "https://~"}),
                "text_key": ("STRING", {"multiline": False, "default": "content"}),
                "text_value": ("STRING", {"multiline": False, "default": "Hello, World!!"}),
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ()
    FUNCTION = "run"
    CATEGORY = "RequestSettings"

    def run(self, text_url, text_key, text_value, image):
        url = text_url
        data = {text_key: text_value}
        response = requests.post(url, data=data)

        print(response.status_code)
        print(response.text)
        return (response.text)

NODE_CLASS_MAPPINGS = {
    "PostRequests": PostRequests,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RequestsPoster": "PostRequests",
}