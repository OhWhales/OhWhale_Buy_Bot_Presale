import web3
import requests
import threading
import asyncio
from telegram import Bot

# WebSocket URLs for Alchemy
alchemy_bsc_wss_url = "YOUR_BSC_WSS_URL"  # Replace with your BSC WebSocket URL
alchemy_eth_wss_url = "YOUR_ETH_WSS_URL"  # Replace with your Ethereum WebSocket URL

# Connecting to BSC and Ethereum networks
w3_bsc = web3.Web3(web3.Web3.LegacyWebSocketProvider(alchemy_bsc_wss_url))
w3_eth = web3.Web3(web3.Web3.LegacyWebSocketProvider(alchemy_eth_wss_url))

# Address to monitor (adjust to your contract)
address_to_monitor_bsc = w3_bsc.to_checksum_address("YOUR_BSC_CONTRACT_ADDRESS")
address_to_monitor_eth = w3_eth.to_checksum_address("YOUR_ETH_CONTRACT_ADDRESS")

# Your BscScan and Etherscan API keys
bscscan_api_key = "YOUR_BSCSCAN_API_KEY"
etherscan_api_key = "YOUR_ETHERSCAN_API_KEY"
BSC_SCAN_API_URL = "https://api.bscscan.com/api"
ETHERSCAN_API_URL = "https://api.etherscan.io/api"

# Telegram Bot Token
telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"  # Group chat ID in Telegram where you send notifications

# Telegram Video ID
video_id = "YOUR_TELEGRAM_VIDEO_ID"  # Replace with your video ID

# Creating Telegram Bot object
bot = Bot(token=telegram_token)


async def send_telegram_message(message, video=None):
    """Send a message to Telegram."""
    if video:
        # Send video with a caption as part of the same message
        await bot.send_video(chat_id=chat_id, video=video, caption=message, supports_streaming=True)


def fetch_transaction_receipt(tx_hash, network):
    """Fetch transaction details using eth_getTransactionReceipt."""
    if network == "BSC":
        params = {
            "module": "proxy",
            "action": "eth_getTransactionReceipt",
            "txhash": tx_hash,
            "apikey": bscscan_api_key
        }
        url = BSC_SCAN_API_URL
    else:  # Ethereum
        params = {
            "module": "proxy",
            "action": "eth_getTransactionReceipt",
            "txhash": tx_hash,
            "apikey": etherscan_api_key
        }
        url = ETHERSCAN_API_URL

    response = requests.get(url, params=params)
    try:
        if response.status_code == 200:
            data = response.json()  # Parse JSON
            if "result" in data and data["result"]:
                return data["result"]
            else:
                print(f"No details found for transaction {tx_hash} on {network}.")
        else:
            print(f"API connection error. HTTP Code: {response.status_code}")
    except requests.exceptions.JSONDecodeError:
        print("Error parsing the API response. The response is not a valid JSON.")
    return None


def analyze_receipt(receipt, network):
    """Analyze transaction details and logs."""
    if receipt:
        try:
            # Check logs and extract data about token purchases
            if "logs" in receipt and receipt["logs"]:
                for log in receipt["logs"]:
                    # Check the log for token purchases
                    if log['address'].lower() == "YOUR_CONTRACT_ADDRESS".lower():
                        # Read who bought and how many tokens (tokensBought)
                        buyer = '0x' + log['topics'][1][26:]  # Remove leading zeros
                        tokens_bought = int(log['topics'][2], 16)  # Number of tokens purchased

                        # Calculate the amount spent in USD (price of each token is 0.014 USD)
                        amount_spent = tokens_bought * 0.014

                        # Base message for the purchase
                        message = f"Oh Whale Presale Buy !💰🐳\n\n" \
                                  f"🐋 Bought: {tokens_bought} $OHW\n" \
                                  f"💵 Amount Spent: ${amount_spent:.2f} USD\n\n" \
                                  f"🌊 Together we making waves 🌊💙"

                        # Add special message if the purchase is 71428 or more
                        if tokens_bought >= 71428:
                            message += "\n\n🎉 **Congrats on securing your Early Supporter NFT allocation!** 🎉\n"

                        # Send the message to Telegram
                        asyncio.run(send_telegram_message(message, video=video_id))

        except Exception as e:
            print(f"Error analyzing transaction on {network}: {e}")
    else:
        print(f"No data to analyze on {network}.")


def handle_event(event, network):
    """Process a new event."""
    tx_hash = event["transactionHash"].hex()
    print(f"\nDetected new event on {network}, transaction hash: {tx_hash}")

    # Fetch transaction details
    receipt = fetch_transaction_receipt(tx_hash, network)
    analyze_receipt(receipt, network)


def log_loop_bsc():
    """Event listening loop for BSC."""
    subscription_bsc = w3_bsc.eth.filter({
        "fromBlock": "latest",
        "address": address_to_monitor_bsc
    })

    print(f"Listening for events on BSC address: {address_to_monitor_bsc}")

    while True:
        try:
            events = subscription_bsc.get_new_entries()
            for event in events:
                handle_event(event, "BSC")
        except Exception as e:
            print(f"Error listening on BSC: {e}")


def log_loop_eth():
    """Event listening loop for Ethereum."""
    subscription_eth = w3_eth.eth.filter({
        "fromBlock": "latest",
        "address": address_to_monitor_eth
    })

    print(f"Listening for events on Ethereum address: {address_to_monitor_eth}")

    while True:
        try:
            events = subscription_eth.get_new_entries()
            for event in events:
                handle_event(event, "Ethereum")
        except Exception as e:
            print(f"Error listening on Ethereum: {e}")


# Start monitoring in two threads
def start_monitoring():
    thread_bsc = threading.Thread(target=log_loop_bsc)
    thread_eth = threading.Thread(target=log_loop_eth)

    thread_bsc.start()
    thread_eth.start()

    thread_bsc.join()
    thread_eth.join()


if __name__ == "__main__":
    start_monitoring()
