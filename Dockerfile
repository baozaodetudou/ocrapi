FROM ubuntu:latest
ENV LANG="C.UTF-8" \
    TZ="Asia/Shanghai" \
    REPO_URL="https://github.com/jxxghp/nas-tools-ocr.git" \
    WORKDIR="/app"
WORKDIR ${WORKDIR}
RUN apt-get update && apt-get install -y ffmpeg libgomp1 libsm6 libxrender1 libxext6 libgl1 python3 python3-pip
RUN git clone -b main ${REPO_URL} ${WORKDIR}
RUN pip3 install -r requirements.txt
EXPOSE 9899
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]