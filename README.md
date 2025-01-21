# Ethereum Faucet API

This is a Django-based API for an Ethereum faucet. The faucet allows users to request test Ether for development purposes. 

## Environment Variables

The application requires the following environment variables to be set:

| Variable            | Description                                                                         | Example Value                                     |
|---------------------|-------------------------------------------------------------------------------------|---------------------------------------------------|
| `RPC_ADDRESS`       | RPC Address for the Ethereum endpoint.                                              | `https://mainnet.infura.io/v3/YOUR_PROJECT_ID`    |
| `FUND_TIMEOUT`      | Timeout period (in seconds) to prevent repeated funding requests.                   | `3600` (1 hour)                                   |
| `FUND_AMOUNT_WEI`   | Amount of WEI to send from the faucet per request.                                  | `1000000000000000000` (1 ETH)                     |
| `WHALE_PRIVATE_KEY` | Private key of the funding account.                                                 | `0xYOUR_PRIVATE_KEY`                              |
| `DB_PATH`           | Folder where the SQLite3 database file is created. If empty, the app dir is used    | `./data`                                          |

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/daniel1302/python-ethereum-faucet.git
    cd python-ethereum-faucet
    ```

2. Create and activate a virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Export the following environment variable

    ```env
    RPC_ADDRESS=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
    FUND_TIMEOUT=3600
    FUND_AMOUNT_WEI=1000000000000000000
    WHALE_PRIVATE_KEY=0xYOUR_PRIVATE_KEY
    DB_PATH=./data
    ```

5. Apply migrations:

    ```bash
    python manage.py migrate
    ```

6. Run the development server:

    ```bash
    python manage.py runserver
    ```

## Docker development

```shell
docker build -t faucet ./ 
docker run \
    -e WHALE_PRIVATE_KEY="0xYOUR_PRIVATE_KEY" \
    -e DB_PATH=/data \
    -v /data:/data \
    -p 8000:8000 \
    faucet
```

## Usage

The API exposes endpoints for interacting with the faucet. Use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/) to send requests to the API.

### Example Request

To request Ether from the faucet:

```http
POST /faucet/fund
Content-Type: application/json

{
    "address": "0xRecipientAddressHere"
}
```

To get statistics about the transactions:

```http
GET /faucet/stats

{
    "successful_txs": 110, 
    "failed_txs": 2
}
```

To get info about environment settings(secrets are not returned, all secrets are obfuscated):

```http
GET /faucet/environment

{
    "RPC_ADDRESS": "http:/...", 
    "FUND_TIMEOUT": 60, 
    "FUND_AMOUNT_WEI": 0.1, 
    "WHALE_PRIVATE_KEY": "0x00b9..."
}
```

### Example Response

```json
{
    "tx_hash": "0xTransactionHashHere"
}
```



## Notes

- Ensure your funding account (`WHALE_PRIVATE_KEY`) is loaded with sufficient Ether for test transactions.
- The database path (`DB_PATH`) should be writable by the application.
- Use a secure way to store and manage your private keys.

## Contributing

1. Fork the repository.
2. Create a new branch:

    ```bash
    git checkout -b feature-name
    ```

3. Commit your changes:

    ```bash
    git commit -m "Description of changes"
    ```

4. Push to the branch:

    ```bash
    git push origin feature-name
    ```

5. Open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For issues or inquiries, please open an issue on the [GitHub repository](https://github.com/your-username/ethereum-faucet).
