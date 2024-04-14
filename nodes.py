import requests
import tweepy
import json
import folder_paths
import numpy as np
import os
from PIL import Image
from datetime import datetime

# AnyType ***********************************************************************************
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any = AnyType("*")

# ImageSaver ***********************************************************************************
class ImageSaver:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    # 画像を保存する関数(SaveImageをコピペした)
    def SaveAndGetImagePath(self, images, filename_prefix):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(
            filename_prefix, 
            self.output_dir, 
            images[0].shape[1], 
            images[0].shape[0]
        )

        # 最初の画像のみ保存する
        image = images[0]
        i = 255. * image.cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
        metadata = None

        filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
        fullpath = os.path.join(full_output_folder, filename)
        img.save(fullpath, pnginfo=metadata, compress_level=self.compress_level)

        return fullpath

# PostText ***********************************************************************************
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

# PostImage2X ***********************************************************************************
class PostImage2X:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "PostImage2X"}),
                "text_message": ("STRING", {"multiline": True, "default": "Image generation is complete."}),
                "text_consumer_key": ("STRING", {"multiline": False}),
                "text_consumer_secret": ("STRING", {"multiline": False}),
                "text_access_token": ("STRING", {"multiline": False}),
                "text_access_token_secret": ("STRING", {"multiline": False}),
                "fsfo": ("BOOLEAN", {"default": False}), #for_super_followers_only
            },
        }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    CATEGORY = "RequestsPoster"

    # Xに投稿する関数
    def run(self, images, text_message, fsfo, 
            text_consumer_key, 
            text_consumer_secret, 
            text_access_token, 
            text_access_token_secret, 
            filename_prefix="PostImage2X"):
        # TweepyのAPIオブジェクトを作成
        auth = tweepy.OAuthHandler(text_consumer_key, text_consumer_secret)
        auth.set_access_token(text_access_token, text_access_token_secret)

        # TweepyのAPIとClientオブジェクトを作成
        api = tweepy.API(auth)
        client = tweepy.Client(
            consumer_key = text_consumer_key, 
            consumer_secret = text_consumer_secret, 
            access_token= text_access_token, 
            access_token_secret= text_access_token_secret
        )

        # 画像を保存して投稿
        image_path = ImageSaver().SaveAndGetImagePath(images=images, filename_prefix=filename_prefix)
        message = text_message
        media = api.media_upload(filename=image_path)
        result = client.create_tweet(
            text=message, 
            media_ids=[media.media_id],
            for_super_followers_only=fsfo,
        )
        return ()

# PostImage2Discord ***********************************************************************************
class PostImage2Discord:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", ),
                "filename_prefix": ("STRING", {"default": "PostImage2Discord"}),
                "url": ("STRING", {"multiline": False, "default": "https://~"}),
                "text": ("STRING", {"multiline": True, "default": "Image generation is complete."}),
            },
        }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    CATEGORY = "RequestsPoster"

    # Discordに投稿する関数
    def run(self, images, url, text, filename_prefix="PostImage2Discord"):
        # 画像を保存する
        image_path = ImageSaver().SaveAndGetImagePath(images=images, filename_prefix=filename_prefix)

        # ファイルをバイナリモードで開く
        with open(image_path, 'rb') as f:
            # POSTリクエストを送信
            response = requests.post(
                url,
                files={
                    'file': (image_path, f, 'image/png')
                },
                data={
                    'payload_json': json.dumps({
                        'content': text,
                        'embeds': [{
                            'image': {'url': 'attachment://' + image_path}
                        }]
                    })
                }
            )
        return ()

# Mappings ***********************************************************************************
NODE_CLASS_MAPPINGS = {
    "PostText": PostText,
    "PostImage2X": PostImage2X,
    "PostImage2Discord": PostImage2Discord,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostText": "PostText",
    "PostImage2X": "PostImage2X",
    "PostImage2Discord": "PostImage2Discord",
}