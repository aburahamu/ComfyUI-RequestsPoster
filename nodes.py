import requests
import tweepy
import json
import folder_paths
import numpy as np
import os
import torch
from PIL import Image, ImageOps, ImageSequence
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

# ImageLoader ***********************************************************************************
class ImageLoader:
    # 画像を読み込んで返す関数(LoadImageをコピペした)
    def load_image(self, image_path):
        img = Image.open(image_path)
        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return (output_image, output_mask)

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
                "execute": ("BOOLEAN", {"default": True}),
                },
            }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    CATEGORY = "RequestsPoster"

    def run(self, url, key, value, seed, execute, any):
        if execute:
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
                "images": ("IMAGE", {}),
                "filename_prefix": ("STRING", {"default": "PostImage2X"}),
                "text_message": ("STRING", {"multiline": True, "default": "Image generation is complete."}),
                "text_consumer_key": ("STRING", {"multiline": False}),
                "text_consumer_secret": ("STRING", {"multiline": False}),
                "text_access_token": ("STRING", {"multiline": False}),
                "text_access_token_secret": ("STRING", {"multiline": False}),
                "fsfo": ("BOOLEAN", {"default": False}), #for_super_followers_only,
                "execute": ("BOOLEAN", {"default": True}),
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
            execute,
            filename_prefix="PostImage2X",
            ):
        if execute:
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
                "images": ("IMAGE", {}),
                "filename_prefix": ("STRING", {"default": "PostImage2Discord"}),
                "url": ("STRING", {"multiline": False, "default": "https://~"}),
                "text": ("STRING", {"multiline": True, "default": "Image generation is complete."}),
                "execute": ("BOOLEAN", {"default": True}),
                },
            }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ()

    CATEGORY = "RequestsPoster"

    # Discordに投稿する関数
    def run(self, images, url, text, execute, filename_prefix="PostImage2Discord"):
        if execute:
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

# StableDiffusion3からT2Iで画像を取得 ***********************************************************************************
class GetImageFromSD3byT2I:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "key": ("STRING", {"default": "sk-xxxxx..."}),
                "positive": ("STRING", {"multiline": True, "default": "A painting of a beautiful sunset"}),
                "negative": ("STRING", {"multiline": True, "default": "nsfw, bad quality"}),
                "aspect_ratio": (["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"], {"default": "1:1"}),
                "model": (["sd3", "sd3-turbo"], {"default": "sd3-turbo"}),
                "format": (["png", "jpeg"], {"default": "png"}),
                "seed": ("INT:seed", {}),
            },
        }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE", )

    CATEGORY = "RequestsPoster"

    # 画像の生成と保存
    def run(self, key, positive, negative, aspect_ratio, model, format, seed):
        # 必要なパラメータをセット
        url = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"
        headers_payload = {
            "authorization": f"Bearer {key}",
            "accept": "image/*"
            }
        data_payload = {
            "prompt": f"{positive}",
            "model": f"{model}",
            "aspect_ratio": f"{aspect_ratio}",
            "seed": {seed},
            "output_format": f"{format}",
            }
        # modelがsd3ならネガティブプロンプトを追加
        if model == "sd3":
            data_payload["negative_prompt"] = negative
        
        # 画像生成を指示
        response = requests.post(
            url, 
            headers=headers_payload, 
            files={"none": ''},
            data=data_payload
            )

        # 画像を保存
        filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
        fullpath = os.path.join(self.output_dir, filename)
        if response.status_code == 200:
            with open(f"{fullpath}", 'wb') as file:
                file.write(response.content)
            loader = ImageLoader()
            image, mask = loader.load_image(image_path=fullpath)
        else:
            raise Exception(str(response.json()))
        
        return (image, mask)

# GetImageFromSD3byI2I ***********************************************************************************
class GetImageFromSD3byI2I:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""
        self.compress_level = 4

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {}),
                "key": ("STRING", {"default": "sk-xxxxx..."}),
                "positive": ("STRING", {"multiline": True, "default": "A painting of a beautiful sunset"}),
                "negative": ("STRING", {"multiline": True, "default": "nsfw, bad quality"}),
                "strength": ("FLOAT", {"default": 0.5, "min":0, "max": 1, "step":0.01}),
                "model": (["sd3", "sd3-turbo"], {"default": "sd3-turbo"}),
                "format": (["png", "jpeg"], {"default": "png"}),
                "seed": ("INT:seed", {}),
                "execute": ("BOOLEAN", {"default": True}),
                },
            }

    FUNCTION = "run"
    OUTPUT_NODE = True
    RETURN_TYPES = ("IMAGE",)

    CATEGORY = "RequestsPoster"

    # Discordに投稿する関数
    def run(self, key, positive, images, strength, model, seed, format, negative, execute):
        if execute:
            # 画像のサイズチェック
            img = None
            if images[0].shape[0] >= 64 and images[0].shape[1] >= 64:
                # 画像を保存する
                image_path = ImageSaver().SaveAndGetImagePath(images=images, filename_prefix="SD3I2I")
            else:
                raise Exception(f"画像サイズエラー：画像の縦横サイズを、いずれも64px以上にしてください。")

            # 必要なパラメータをセット
            url = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"
            headers_payload = {
                "authorization": f"Bearer {key}",
                "accept": "image/*"
                }
            data_payload = {
                "prompt": f"{positive}",
                "strength": strength,
                "mode": "image-to-image",
                "model": f"{model}",
                "seed": {seed},
                "output_format": f"{format}",
                }
            # modelがsd3ならネガティブプロンプトを追加
            if model == "sd3":
                data_payload["negative_prompt"] = negative
            
            # 画像生成を指示
            response = requests.post(
                url, 
                headers=headers_payload, 
                files={"image": open(image_path, "rb")},
                data=data_payload
                )

            # 画像を保存
            filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
            fullpath = os.path.join(self.output_dir, filename)
            if response.status_code == 200:
                with open(f"{fullpath}", 'wb') as file:
                    file.write(response.content)
                loader = ImageLoader()
                image, mask = loader.load_image(image_path=fullpath)
            else:
                raise Exception(f"{response.json()}")
            
            return (image, mask)

# Mappings ***********************************************************************************
NODE_CLASS_MAPPINGS = {
    "PostText": PostText,
    "PostImage2X": PostImage2X,
    "PostImage2Discord": PostImage2Discord,
    "GetImageFromSD3byT2I": GetImageFromSD3byT2I,
    "GetImageFromSD3byI2I": GetImageFromSD3byI2I,
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "PostText": "PostText",
    "PostImage2X": "PostImage2X",
    "PostImage2Discord": "PostImage2Discord",
    "GetImageFromSD3byT2I": "GetImageFromSD3byT2I",
    "GetImageFromSD3byI2I": "GetImageFromSD3byI2I",
    }