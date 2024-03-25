FROM alpine:3.19

RUN apk add git
RUN apk add --no-cache python3 py3-pip
RUN git clone https://github.com/CntoDev/discord-owlbot && cd discord-owlbot

CMD ["sh"]