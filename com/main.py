# encoding:UTF-8
# from pipelines import UploadJiePaiPicPipeline
#
# upload = UploadJiePaiPicPipeline()
# url = "https://api2.bmob.cn/2/files/newtest.jpg"
# path = 'C:\\Users\\g8876\\Desktop\\jiepai\\full\\test.jpg'
# upload.uploadImgFile(url,path)
import time

from datetime import datetime, timedelta

result = datetime.now() + timedelta(-1)
print result.strftime("%Y-%m-%d")