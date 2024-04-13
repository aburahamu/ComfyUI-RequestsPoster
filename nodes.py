import requests

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

class PostText:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "url": ("STRING", {"multiline": False, "default": "https://~"}),
                "key": ("STRING", {"multiline": False, "default": "content"}),
                "value": ("STRING", {"multiline": False, "default": "Hello, World!!"}),
                "seed": ("INT:seed", {}),
                "any": (any, {}),
            },
        }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    CATEGORY = "RequestsPoster"

    def run(self, url, key, value, seed, any):
        data = {key: value}
        response = requests.post(url, data)
        print(response)
        return ()

NODE_CLASS_MAPPINGS = {
    "PostText": PostText
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostText": "PostText"
}