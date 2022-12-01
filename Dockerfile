FROM ubuntu:latest
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN apt-get update && apt-get install -y ffmpeg libgomp1 libsm6 libxrender1 libxext6 libgl1 python3 python3-pip
RUN pip3 install -r /code/requirements.txt -i https://mirror.baidu.com/pypi/simple
COPY ./main.py /code/app/main.py
EXPOSE 9899
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]