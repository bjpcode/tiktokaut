import base64
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tiia.v20190529 import tiia_client, models as tiia_models

class AiPlat2(object):
    def __init__(self, secret_id, secret_key):
        self.secret_id = secret_id
        self.secret_key = secret_key

    def detect_label_pro(self, image_path):
        try:
            print("Invoking DetectLabelPro with image:", image_path)  # add logging

            with open(image_path, 'rb') as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()

            cred = credential.Credential(self.secret_id, self.secret_key)
            httpProfile = HttpProfile()
            httpProfile.endpoint = "tiia.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.httpProfile = httpProfile
            client = tiia_client.TiiaClient(cred, "ap-guangzhou", clientProfile)

            req = tiia_models.DetectLabelProRequest()
            params = {
                "ImageBase64": encoded_string,
            }   
            req.from_json_string(json.dumps(params))

            resp = client.DetectLabelPro(req)
            return json.loads(resp.to_json_string())
        except TencentCloudSDKException as err:
            print(err)
            return {'ret': -1, 'msg': str(err)}
