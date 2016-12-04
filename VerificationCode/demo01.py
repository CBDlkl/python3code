import urllib.request, io, pytesseract
from PIL import Image

# 获取网络图片
# urllib.request.urlretrieve(imgUrl, 'Images/01.jpeg')

# 复杂验证码(汉字)
# imgUrl = 'http://gsxt.saic.gov.cn/zjgs/captcha?preset=&ra=0.6409699235539787'

# 稍复杂的验证码
# imgUlr = 'https://passport.csdn.net/ajax/verifyhandler.ashx'

# 简单验证码
imgUrl = 'http://wsdj.baic.gov.cn/system/getVerifyCode.do?Sun%20Dec%2004%202016%2017:55:12%20GMT+0800%20(CST)'

response = urllib.request.urlopen(imgUrl)

tmpImg = io.BytesIO(response.read())

im = Image.open(tmpImg)

im.show()

vCode = pytesseract.image_to_string(im)

print(im.size, vCode)
