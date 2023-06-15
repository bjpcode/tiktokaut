import base64

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.tiia.v20190529 import tiia_client, models

def main():
    try:
        # Encode local image to base64
        with open("C:/Users/baij/Desktop/WishfulIT/python自动刷号设定/Douyin-Bot/autojump.png", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Instantiate an authentication object. The Tencent Cloud account `secretId` and `secretKey` need to be replaced with your own.
        cred = credential.Credential("AKIDW0HNErJXWGsHSs56sPltpX2KNE0Yrysc", "ax84mGVihRxFMJ2Yw85oLfldLuJWXN6c")

        # Instantiate a client request profile and specify the endpoint.
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tiia.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        # Instantiate the client object to request the product and the specific API.
        client = tiia_client.TiiaClient(cred, "ap-guangzhou", clientProfile) 

        # Instantiate a request object.
        req = models.DetectLabelProRequest()

        # Fill in each field of the request structure. Note: The field may be empty, so it can be left as is. The specific request field is in the `request` model.
        params = '{"ImageBase64":"' + encoded_string + '"}'
        req.from_json_string(params)

        # Return the request object as a dictionary.
        resp = client.DetectLabelPro(req) 
        print(resp.to_json_string()) 

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
