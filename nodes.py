import requests

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

class PostRequests:
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
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "RequestsPoster"

    def run(self, url, key, value, seed, any):
        data = {key: value}
        response = requests.post(url, data)
        print(response)
        return ()

NODE_CLASS_MAPPINGS = {
    "PostRequests": PostRequests,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostRequests": "PostRequests",
}