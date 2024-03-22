FROM selenium/standalone-chrome:122.0

WORKDIR /app

COPY ./requirements.txt ./

USER root

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY ./PricePredictor.py /app

CMD ["python3", "/app/PricePredictor.py"]


