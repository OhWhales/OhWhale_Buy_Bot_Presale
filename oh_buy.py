import web3
import requests
import threading
import asyncio
from telegram import Bot

# WebSocket URLs for Alchemy
alchemy_bsc_wss_url = "wss://YOUR_ALCHEMY_BSC_WSS_URL"
alchemy_eth_wss_url = "wss://YOUR_ALCHEMY_ETH_WSS_URL"

# Connecting to BSC and Ethereum networks
w3_bsc = web3.Web3(web3.Web3.LegacyWebSocketProvider(alchemy_bsc_wss_url))
w3_eth = web3.Web3(web3.Web3.LegacyWebSocketProvider(alchemy_eth_wss_url))

# Address to monitor
address_to_monitor_bsc = w3_bsc.to_checksum_address("0xYOUR_BSC_ADDRESS")
address_to_monitor_eth = w3_eth.to_checksum_address("0xYOUR_ETH_ADDRESS")

# Telegram setup
telegram_token = "YOUR_TELEGRAM_BOT_TOKEN"
chat_id = "YOUR_TELEGRAM_CHAT_ID"
video_id = "YOUR_TELEGRAM_VIDEO_ID"
bot = Bot(token=telegram_token)


async def send_telegram_message(message, video=None):
    """Send a message to Telegram."""
    if video:
        await bot.send_video(chat_id=chat_id, video=video, caption=message, supports_streaming=True)
    else:
        await bot.send_message(chat_id=chat_id, text=message)


def fetch_transaction_receipt(tx_hash, network):
    """Fetch transaction details."""
    api_key = "YOUR_BSCSCAN_API_KEY" if network == "BSC" else "YOUR_ETHERSCAN_API_KEY"
    base_url = "https://api.bscscan.com/api" if network == "BSC" else "https://api.etherscan.io/api"
    params = {"module": "proxy", "action": "eth_getTransactionReceipt", "txhash": tx_hash, "apikey": api_key}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json().get("result")
    print(f"Error fetching transaction receipt for {tx_hash} on {network}: {response.status_code}")
    return None


def analyze_receipt(receipt, network):
    """Analyze and process transaction receipt."""
    if receipt and "logs" in receipt:
        for log in receipt["logs"]:
            if log["address"].lower() == address_to_monitor_bsc.lower():
                buyer = "0x" + log["topics"][1][26:]
                tokens_bought = int(log["topics"][2], 16)
                amount_spent = tokens_bought * 0.014

                message = (
                    f"Oh Whale Presale Buy! 💰🐳\n\n"
                    f"🐋 Bought: {tokens_bought} $OHW\n"
                    f"💵 Amount Spent: ${amount_spent:.2f} USD\n\n"
                    f"🌊 Together we make waves 🌊💙"
                )
                if tokens_bought >= 71428:
                    message += "\n\n🎉 **Congrats on securing your Early Supporter NFT allocation!** 🎉"

                loop = asyncio.get_event_loop()
                loop.run_until_complete(send_telegram_message(message, video=video_id))
    else:
        print(f"No valid logs found in receipt on {network}.")


def handle_event(event, network):
    """Handle blockchain events."""
    tx_hash = event["transactionHash"].hex()
    print(f"Detected new event on {network}, transaction hash: {tx_hash}")
    receipt = fetch_transaction_receipt(tx_hash, network)
    analyze_receipt(receipt, network)


def event_listener(w3_instance, address, network):
    """Listen for events on a blockchain."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    subscription = w3_instance.eth.filter({"fromBlock": "latest", "address": address})
    print(f"Listening for events on {network} address: {address}")

    while True:
        try:
            events = subscription.get_new_entries()
            for event in events:
                handle_event(event, network)
        except Exception as e:
            print(f"Error in {network} listener: {e}")


def start_monitoring():
    """Start monitoring threads."""
    bsc_thread = threading.Thread(target=event_listener, args=(w3_bsc, address_to_monitor_bsc, "BSC"))
    eth_thread = threading.Thread(target=event_listener, args=(w3_eth, address_to_monitor_eth, "Ethereum"))

    bsc_thread.start()
    eth_thread.start()

    bsc_thread.join()
    eth_thread.join()


if __name__ == "__main__":
    start_monitoring()
