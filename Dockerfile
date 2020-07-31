FROM python:3.7-alpine

COPY bots/code.py /bots/
COPY bots/four.py /bots/
COPY requirements.txt /tmp
COPY bots/config.ini /bots/
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "code.py"]
