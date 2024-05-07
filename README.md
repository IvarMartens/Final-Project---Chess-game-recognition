# Chess Game Recognition
:triangular_flag_on_post: The goal of this project is to be able to do a live demonstration where we regocnise the pieces on a chess board and their location using your phone camera. This can be devided into three sub goals:
1. At least chess game reconstruction with a single camera from a fixed position.
2. Chess game reconstruction from multiple angels.
3. Free-hand video chess game reconstruction.



## Requirements 
All the requirements for this project are listed in the requirements.txt file. These packages can be intalled using `pip install requirements.txt`.

## Camera feed
In order to use the camera feed from your phone you have to follow the following steps:
1. Download an app such as "IP Webcam" for Android or "iVCam" for iOS and Windows
2. Start a stream in the "IP Webcam app"
3. Change the location in the helper.get_ip() fuction (make sure the location is added in the helper.py file)
```python
import helper

video_feed_url = helper.get_ip('home')
cap = cv2.VideoCapture(video_feed_url)
```

## Interesting links
- https://blog.roboflow.com/chess-boards/
- https://github.com/georg-wolflein/chesscog
