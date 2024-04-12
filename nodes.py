import requests

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
                "image": ("IMAGE",),
            }
        }

    RETURN_TYPES = ()
    OUTPUT_NODE = True
    FUNCTION = "run"
    CATEGORY = "RequestsPoster"

    def run(self, url, key, value, image):
        data = {key: value}
        response = requests.post(url, data)

        print(response.status_code)
        print(response.text)
        return ()

NODE_CLASS_MAPPINGS = {
    "PostRequests": PostRequests,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostRequests": "PostRequests",
}

#PostRequests.run(
#    "",
#    "https://discord.com/api/webhooks/1228320912701390888/vkaex8-k7PL88S2d70jApzVILpFhaYkzvgrbh9w1rKZGixA-9zTt178lVJam_6khHMN3",
#    "content",
#    "Test, World!!",
#    "test"
#)