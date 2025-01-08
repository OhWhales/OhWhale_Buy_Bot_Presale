
# OhWhale Presale Bot

## Overview
The OhWhale Presale Bot is designed to monitor token purchases on both Binance Smart Chain (BSC) and Ethereum networks. The bot listens for new transactions and sends notifications to a Telegram group chat with details about the purchase. It also congratulates users who make substantial token purchases by rewarding them with Early Supporter NFT allocations.

The bot is part of **[Oh Whale](https://ohwhale.io)**, a project dedicated to protecting the real oceans and contribute to the digital ones through blockchain technology.

---

## Key Features
- Monitors **Binance Smart Chain (BSC)** and **Ethereum** networks for token purchases.
- Sends detailed notifications to a **Telegram bot** with purchase details.
- Includes a special congratulatory message for users who purchase a substantial amount of tokens.
- Displays clickable links to the **OhWhale website** and **whitepaper**.
- Uses **Alchemy WebSocket** for real-time transaction monitoring.

---

## Getting Started

### Prerequisites
- Python 3.x
- Telegram Bot API token
- BscScan and Etherscan API keys for fetching transaction receipts
- Alchemy WebSocket URLs for BSC and Ethereum networks

### Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ohwhale-presale-bot.git
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Replace the placeholders in the code with your actual:
   - **Telegram Bot API token**
   - **BscScan and Etherscan API keys**
   - **Alchemy WebSocket URLs**
   - **Contract address for monitoring**

4. Run the bot:
   ```bash
   python Buy_Bot_Presale.py
   ```

---
### Hosting and Costs

The **OhWhale Presale Buy Bot** can be easily hosted on the **PythonAnywhere** platform, which offers a **$5/month** plan that is more than sufficient to run this script efficiently. This makes the bot accessible to users on a budget.

- **PythonAnywhere** (5$ plan):
  - Ideal for running small Python scripts like this bot.
  - Perfect for maintaining WebSocket connections and running continuous monitoring on Ethereum and BSC networks.
  - **Monthly cost**: **$5 (plus VAT)** – Total: **$6.50/month** including VAT.

Additionally, the bot utilizes **Alchemy**'s **free-tier WebSocket plan**, which provides enough capacity for moderate usage. Alchemy offers free access to WebSocket URLs for Ethereum and BSC networks, which is sufficient for the OhWhale Presale Buy Bot.

- **Alchemy** (Free-tier plan):
  - Free access to WebSocket URLs for Ethereum and Binance Smart Chain (BSC).
  - Provides sufficient usage for tracking and receiving real-time events without incurring additional costs.

---
## Mission of Oh Whale 🐋

At **[Oh Whale](https://ohwhale.io)**, we are dedicated to preserving the oceans and protecting marine life, including whales, by leveraging blockchain technology. We not only aim to contribute to the physical preservation of our oceans but also to create a **digital ocean** in the blockchain space, where sustainability, community, and technology converge.

By supporting **OhWhale.io**, you are helping make a difference in both the real and digital worlds.

---

## Contributing

We welcome contributions from the community. If you'd like to contribute, please follow these steps:
1. Fork this repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

---

## License
This project is licensed under the MIT License.
