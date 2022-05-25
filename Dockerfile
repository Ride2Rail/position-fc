FROM python:3.8

ENV APP_NAME=position.py
COPY /code/"$APP_NAME" /code/"$APP_NAME"
COPY /code/position.conf /code/position.conf
COPY /code/utils_position.py /code/utils_position.py

WORKDIR /code


ENV FLASK_APP="$APP_NAME"
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip3 install --no-cache-dir pip==22.1.1

COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5007

CMD ["flask", "run"]
