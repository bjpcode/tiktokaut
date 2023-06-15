import base64
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.iai.v20200303 import iai_client, models

def test_api_with_image(image_path):
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    cred = credential.Credential("yourid", "yourkey") 
    httpProfile = HttpProfile()
    httpProfile.endpoint = "iai.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = iai_client.IaiClient(cred, "ap-guangzhou", clientProfile) 

    req = models.DetectFaceRequest()
    params = {
        "Image": encoded_string,
        "MaxFaceNum": 1,
        "MinFaceSize": 40,  # You can adjust this value according to your requirement
        "FaceModelVersion": "3.0",
        "NeedFaceAttributes": 1,
        "NeedQualityDetection": 1
    }
    req.from_json_string(json.dumps(params))
    try:
        rsp = client.DetectFace(req) 
        print(rsp.to_json_string())
    except Exception as e:
        print(f"An error occurred: {e}")
    

# replace 'YOUR_IMAGE_PATH' with your actual image path
test_api_with_image('C:/Users/baij/Desktop/WishfulIT/python自动刷号设定/Douyin-Bot/face/new.png')
