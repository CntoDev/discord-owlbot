FROM alpine:3.19

ADD . /owlbot
WORKDIR /owlbot

RUN apk add --no-cache python3 py3-pip
RUN pip install --break-system-packages -r requirements.txt

# Install tzdata to switch timezone on deployment
RUN apk add --no-cache tzdata

CMD ["python", "owlbot.py"]