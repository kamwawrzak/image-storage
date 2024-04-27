FROM python:3.12

WORKDIR /app

COPY . /app

RUN make install-deps

EXPOSE 8080

CMD [ "make", "run-server" ]
