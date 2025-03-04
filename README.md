# Telegram Expense Tracker Bot

This bot collects user input from Telegram chats and records expenses into a predefined Google Sheets template for monthly tracking.

## 🚀 Features
- Accepts expense details from users in a structured format.
- Stores data in a Google Sheets template.
- Supports multiple users with separate records.
- Provides quick summaries of expenses upon request.

## 🛠️ Setup Instructions

### 1️⃣ Prerequisites
- Python 3.8+
- A Telegram bot token (get it from [@BotFather](https://t.me/BotFather))
- A Google Cloud project with enabled Google Sheets API
- A service account with access to your Google Sheet

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
