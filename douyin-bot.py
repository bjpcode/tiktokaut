import sys
import random
import time
from PIL import Image
import argparse

if sys.version_info.major != 3:
    print('Please run under Python3')
    exit(1)

try:
    from common import debug, config, screenshot, UnicodeStreamFilter
    from common.auto_adb import auto_adb
    from common import apiutil
    from common import apiutil2
    from common.compression import resize_image
except Exception as ex:
    print(ex)
    print('Please place the script in the root directory of the project')
    print('Please check if the "common" folder exists in the root directory of the project')
    exit(1)

VERSION = "0.0.1"

AppID = 'your-id'
AppKey = 'your-key'

DEBUG_SWITCH = True
FACE_PATH = 'face/'

adb = auto_adb()
adb.test_device()
config = config.open_accordant_config()

BEAUTY_THRESHOLD = 70

GIRL_MIN_AGE = 16

def yes_or_no():
    """
    Check if the user is ready to start the program
    """
    while True:
        yes_or_no = str(input('Please make sure the phone has opened ADB and connected to the computer,'
                              'then open the phone software, confirm to start? [y/n]:'))
        if yes_or_no == 'y':
            break
        elif yes_or_no == 'n':
            print('Thanks for using')
            exit(0)
        else:
            print('Please input again')

def _random_bias(num):
    """
    random bias
    :param num:
    :return:
    """
    return random.randint(-num, num)

def next_page():
    """
    Flip to the next page
    :return:
    """
    cmd = 'shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=config['center_point']['x'],
        y1=config['center_point']['y']+config['center_point']['ry'],
        x2=config['center_point']['x'],
        y2=config['center_point']['y'],
        duration=200
    )
    adb.run(cmd)
    time.sleep(1.5)

def follow_user():
    """
    Follow the user
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['follow_bottom']['x'] + _random_bias(10),
        y=config['follow_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(2.5)

def thumbs_up():
    """
    Like the post
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['star_bottom']['x'] + _random_bias(10),
        y=config['star_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0)

# Reply to a comment
def reply():
    """
    Reply to the comment
    :return:
    """
    cmd = 'shell input tap {x} {y}'.format(
        x=config['comment_bottom']['x'] + _random_bias(10),
        y=config['comment_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)

    msg_list = ['I love it', 'Great', 'Nice', 'Amazing', 'So cool', 'Beautiful', 'Fantastic', 'Good job', 'Keep going']

    cmd = 'shell am broadcast -a ADB_INPUT_TEXT --es msg {msg}'.format(
        msg=random.choice(msg_list)
    )
    adb.run(cmd)
    time.sleep(0.5)

    cmd = 'shell input tap {x} {y}'.format(
        x=config['comment_send_bottom']['x'] + _random_bias(10),
        y=config['comment_send_bottom']['y'] + _random_bias(10)
    )
    adb.run(cmd)
    time.sleep(0.5)

def main():
    """
    The main function
    :return: None
    """
    yes_or_no()

    ai_obj = apiutil.AiPlat(AppID, AppKey)
    ai_obj2 = apiutil2.AiPlat2(AppID, AppKey)

    while True:
       
        screenshot.check_screenshot()
   
        img = screenshot.pull_screenshot()
        if img is None:
            print("Failed to capture screenshot.")
            sys.exit(1)

      
        img_path = "screenshot.png"
        img.save(img_path)

        
        new_img_path = FACE_PATH + 'new.png'
        resize_image(img_path, new_img_path, 1000000)  


        rsp = ai_obj.invoke_with_sdk(new_img_path)
        print(rsp)
        if rsp and 'FaceInfos' in rsp:
            beauty = 0
            age = 0
            faces = rsp.get('FaceInfos', [])
            if faces:
                for face in faces:
                    beauty = face.get('FaceAttributesInfo', {}).get('Beauty')
                    age = face.get('FaceAttributesInfo', {}).get('Age')

                print('Beauty: {}, Age: {}'.format(beauty, age))

                if beauty > BEAUTY_THRESHOLD and age > GIRL_MIN_AGE:
                    thumbs_up()

                    #follow_user()

                    #if args.reply:
                    #y
                    #     reply()
            else:
                print('No faces detected.')

        else:
            print("Face detection failed. Error code:", rsp.get('ret') if rsp and 'ret' in rsp else None)
        rsp2 = ai_obj2.detect_label_pro(new_img_path) 
        print(rsp2)  

        next_page()

parser = argparse.ArgumentParser()
parser.add_argument('--reply', default=False, action=argparse.BooleanOptionalAction,
                    help='auto reply message, default is False')

args = parser.parse_args()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
