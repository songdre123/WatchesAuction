
FROM python:3-slim

WORKDIR /app

COPY auction_requirements.txt ./

RUN python -m pip install --no-cache-dir -r auction_requirements.txt

COPY ./Auction.py .

CMD [ "python", "Auction.py" ]

