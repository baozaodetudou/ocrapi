import base64
import io
import re
import cv2
import uvicorn
import numpy as np
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel
from paddleocr import PaddleOCR
# from matplotlib import pyplot as plt

app = FastAPI()
# Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
ocr = PaddleOCR(use_angle_cls=True, lang="ch")


class OCR(BaseModel):
    base64_img: str


@app.get("/")
async def root():
    return {"message": "paddleocr API"}


@app.post("/captcha/base64")
async def captcha_base64(data: OCR):
    base64_img = data.dict().get("base64_img")
    img_b = base64.b64decode(base64_img.encode('utf-8'))
    img = Image.open(io.BytesIO(img_b)).convert("RGB")
    mask_npl = np.array(img, dtype=np.uint8)
    # plt.imshow(mask_npl)
    # plt.show()
    ret, thresh = cv2.threshold(mask_npl, 1, 255, cv2.THRESH_BINARY)
    # plt.imshow(thresh)
    # plt.show()
    thresh1 = noise_unsome_piexl(thresh)
    # plt.imshow(thresh1)
    # plt.show()
    # im1 = operate_img(thresh, 4)
    # plt.imshow(im1)
    # plt.show()
    grayImage = around_white(thresh1)
    # plt.imshow(grayImage)
    # plt.show()

    results = ocr.ocr(grayImage, cls=True)
    try:
        result = ''.join(re.findall(r'[A-Za-z0-9]', results[0][0][1][0]))
    except Exception as e:
        print(str(e))
        result = ''
    return {"res": result}


# 四周置白色
def around_white(img):
    w, h, s = img.shape
    for _w in range(w):
        for _h in range(h):
            if (_w <= 5) or (_h <= 5) or (_w >= w-5) or (_h >= h-5):
                img.itemset((_w, _h, 0), 255)
                img.itemset((_w, _h, 1), 255)
                img.itemset((_w, _h, 2), 255)
    return img


# 邻域非同色降噪
def noise_unsome_piexl(img):
    '''
        查找像素点上下左右相邻点的颜色，如果是非白色的非像素点颜色，则填充为白色
    '''
    # print(img.shape)
    w, h, s = img.shape
    for _w in range(w):
        for _h in range(h):
            if _h != 0 and _w != 0 and _w < w - 1 and _h < h - 1:# 剔除顶点、底点
                center_color = img[_w, _h] # 当前坐标颜色
                # print(center_color)
                top_color = img[_w, _h + 1]
                bottom_color = img[_w, _h - 1]
                left_color = img[_w - 1, _h]
                right_color = img[_w + 1, _h]
                cnt = 0
                if top_color.all() == center_color.all():
                    cnt += 1
                if bottom_color.all() == center_color.all():
                    cnt += 1
                if left_color.all() == center_color.all():
                    cnt += 1
                if right_color.all() == center_color.all():
                    cnt += 1
                if cnt < 1:
                    img.itemset((_w, _h, 0), 255)
                    img.itemset((_w, _h, 1), 255)
                    img.itemset((_w, _h, 2), 255)
    return img


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=9899, reload=False)
