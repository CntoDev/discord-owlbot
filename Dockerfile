FROM alpine:3.19

RUN apk add git
RUN apk add --no-cache python3 py3-pip
RUN git clone https://github.com/CntoDev/discord-owlbot
RUN cd discord-owlbot && pip install --break-system-packages -r requirements.txt
RUN crontab discord-owlbot/crontab.txt


CMD ["sh"]