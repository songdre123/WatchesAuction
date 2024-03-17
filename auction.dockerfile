FROM python:3-slim
WORKDIR /usr/src/app
COPY auction_requirements.txt ./
RUN python -m pip install --no-cache-dir -r auction_requirements.txt
COPY ./Auction.py .
COPY ./config.ini /usr/src/app/config.ini
CMD [ "python", "./Auction.py" ]
