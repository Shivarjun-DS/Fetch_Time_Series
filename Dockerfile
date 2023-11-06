FROM python:3.10.9-slim
RUN pip install -U pip
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD [ "python", "./prediction.py"]