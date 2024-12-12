FROM --platform=$TARGETPLATFORM python:alpine as build_bin
WORKDIR /code
RUN mkdir /code/clash_crontab_update
# 复制源文件
COPY clash_crontab_update /code/clash_crontab_update/
RUN python -m zipapp -p "/usr/bin/env python3" clash_crontab_update

FROM --platform=$TARGETPLATFORM python:alpine as build_img
# COPY pip.conf /etc/pip.conf
RUN pip --no-cache-dir install --upgrade pip
WORKDIR /code
COPY requirements.txt /code/requirements.txt
RUN python -m pip --no-cache-dir install -r requirements.txt
COPY --from=build_bin /code/clash_crontab_update.pyz /code
CMD ["python" ,"clash_crontab_update.pyz"]