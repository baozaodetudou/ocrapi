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
    ret, thresh1 = cv2.threshold(mask_npl, 1, 255, cv2.THRESH_BINARY)
    results = ocr.ocr(thresh1, cls=True)
    try:
        result = ''.join(re.findall(r'[A-Za-z0-9]', results[0][0][1][0]))
    except Exception as e:
        print(str(e))
        result = ''
    return {"res": result}


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=9899, reload=False)
