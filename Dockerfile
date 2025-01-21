FROM python:3.10-bookworm

ENV RPC_ADDRESS="http://sepolia1.local.mainnet.community:8545"
ENV FUND_TIMEOUT="60"
ENV FUND_AMOUNT_WEI="100000000000000000"
ENV WHALE_PRIVATE_KEY="missing_key"
ENV DJANGO_DEBUG=False
ENV DB_PATH="/app"

EXPOSE 8000

COPY . /app
COPY ./entrypoint.sh /entrypoint.sh

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["gunicorn", "faucet.wsgi", "--bind", "0.0.0.0:8000"]