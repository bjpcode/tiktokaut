import base64
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.iai.v20200303 import iai_client, models


class AiPlat(object):
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key

    def invoke_with_sdk(self, image_path):
        try:
            print("Invoking face detection with image:", image_path)  # add logging

            with open(image_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()

            cred = credential.Credential(self.secret_id, self.secret_key)
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

            resp = client.DetectFace(req)
            return json.loads(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)
            return {'ret': -1, 'msg': str(err)}