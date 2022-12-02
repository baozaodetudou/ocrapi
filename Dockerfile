FROM ubuntu:latest
ENV LANG="C.UTF-8" \
    TZ="Asia/Shanghai" \
    REPO_URL="https://github.com/jxxghp/nas-tools-ocr.git" \
    WORKDIR="/app"
WORKDIR ${WORKDIR}
RUN apt-get update && apt-get install -y ffmpeg libgomp1 libsm6 libxrender1 libxext6 libgl1 python3 python3-pip
RUN python_ver=$(python3 -V | awk '{print $2}') \
    && echo "${WORKDIR}/" > /usr/lib/python${python_ver%.*}/site-packages/nas-tools.pth \
    && git config --global pull.ff only \
    && git clone -b master ${REPO_URL} ${WORKDIR} \
    && git config --global --add safe.directory ${WORKDIR} \
RUN pip3 install -r requirements.txt
EXPOSE 9899
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]