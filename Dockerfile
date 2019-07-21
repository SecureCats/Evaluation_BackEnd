FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

RUN sed -i 's/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org/debian-security|mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list && \
    sed -i 's|security.debian.org|mirrors.tuna.tsinghua.edu.cn/debian-security|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y nginx supervisor libgmp3-dev libmpfr-dev yarn libmpc-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt --no-cache-dir && \
    yarn global add @vue/cli @vue/cli-service @vue/cli-plugin-unit-jest && \
    cd Evaluation_FrontEnd && yarn install && yarn build --frozen-lockfile && cd .. \
    rm -rf /var/lib/apt/lists/* && \
    echo "daemon off;" >> /etc/nginx/nginx.conf && \
    python manage.py collectstatic --noinput

ENV DEBUG False
COPY deploy/nginx-app.conf /etc/nginx/sites-available/default
COPY deploy/supervisor-app.conf /etc/supervisor/conf.d/
EXPOSE 80
ENTRYPOINT [ "/bin/bash", "deploy/entrypoint.sh" ]
CMD ["supervisord", "-n"]