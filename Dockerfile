FROM registry.baidubce.com/paddlepaddle/paddle:2.4.0
#
WORKDIR /code
#
COPY ./requirements.txt /code/requirements.txt
#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN hub install ch_pp-ocrv3==1.0.0
#
COPY ./main.py /code/app/main.py
#
EXPOSE 9000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]