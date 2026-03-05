FROM python:3.12.1-alpine3.18

WORKDIR /usr/workspace

RUN apk add --no-cache openjdk11-jre curl tar bash


RUN curl -o allure.tgz -L https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz \
    && mkdir -p /opt \
    && tar -zxvf allure.tgz -C /opt/ \
    && ln -s /opt/allure-2.24.1/bin/allure /usr/bin/allure \
    && rm allure.tgz

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest"]