import requests
import time
import hashlib
import base64
# from bitarray import bitarray
import json

URL = "http://openapi.xfyun.cn/v2/aiui"
APPID = "5b9b70dd"
API_KEY = "92b69ef855cf4c22acc8caba7c742eca"
AUE = "raw"
AUTH_ID = "2894c985bf8b1111c6728db79d3479ae"
DATA_TYPE = "text"
SAMPLE_RATE = "16000"
SCENE = "main"
RESULT_LEVEL = "complete"
LAT = "23.16"
LNG = "113.23"
#个性化参数，需转义
PERS_PARAM = "{\\\"auth_id\\\":\\\"2894c985bf8b1111c6728db79d3479ae\\\"}"
FILE_PATH = "test.txt"


def buildHeader():
    curTime = str(int(time.time()))
    param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\"}"
    #使用个性化参数时参数格式如下：
    #param = "{\"result_level\":\""+RESULT_LEVEL+"\",\"auth_id\":\""+AUTH_ID+"\",\"data_type\":\""+DATA_TYPE+"\",\"sample_rate\":\""+SAMPLE_RATE+"\",\"scene\":\""+SCENE+"\",\"lat\":\""+LAT+"\",\"lng\":\""+LNG+"\",\"pers_param\":\""+PERS_PARAM+"\"}"
    # error: a bytes-like object is required, not 'str'
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    print
    print('type of paramBase64:', type(paramBase64))
    print("(str(paramBase64, 'utf-8')", str(paramBase64, 'utf-8'))
    m2.update((API_KEY + curTime + str(paramBase64, 'utf-8')).encode('utf-8'))
    checkSum = m2.hexdigest()

    # 在 Http Request Header 中配置以下参数用于授权认证
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
    }
    return header

def readFile(filePath):
    binfile = open(filePath, 'rb')
    data = binfile.read()
    print('data in file:', data)
    return data

def request2Aiui(text):
    bintext = str.encode(text)
    r = requests.post(URL, headers=buildHeader(), data=bintext)
    # if you need to post data in file
    # r = requests.post(URL, headers=buildHeader(), data=readFile(FILE_PATH))
    content = r.content
    json_resp = json.loads(content.decode('utf-8'))
    code = json_resp['code']
    if code == '0':
        print('success in response')
        # return the response['data']
        return json_resp['data'][0]
    else:
        # error response
        '''
        {
        "code":"10105",
        "desc":"illegal access|illegal client_ip",
        "data":[],
        "sid":"xxxxxx"
        }
        '''
        #print(json_resp)
        #print(content)
        raise Exception(json_resp)

if __name__ == '__main__':
    try:
        test_text = u'今天的天气怎么样'
        resp = request2Aiui(test_text)
        print(resp)
    except Exception as e:
        print(e.args)