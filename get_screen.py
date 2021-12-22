from PIL import ImageGrab
from PIL import Image
import time
print(time.time())
timeArray = time.localtime(time.time())
print(timeArray)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
print(otherStyleTime)
# 参数说明
# 第一个参数 开始截图的x坐标
# 第二个参数 开始截图的y坐标
# 第三个参数 结束截图的x坐标
# 第四个参数 结束截图的y坐标

bbox = (48, 28, 215, 435)
im = ImageGrab.grab(bbox)
# 参数 保存截图文件的路径
im.save('./as1.png')