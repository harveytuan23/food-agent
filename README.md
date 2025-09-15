# 🤖 Smart Food Management Assistant

An AI-powered food management system based on LangChain and OpenAI, focused on ingredient inventory management with Google Sheets integration and automated notifications.

## ✨ Core Features

### 🥬 Ingredient Management
- **Add Ingredients**: Intelligently parse ingredient information and store in Google Sheets
- **View Inventory**: Display all ingredient inventory status
- **Check Expiration**: Remind about ingredients expiring soon (within 3 days)
- **Reduce Quantity**: Automatically reduce inventory when using ingredients
- **Delete Ingredients**: Completely remove unwanted ingredients
- **Update Ingredients**: Modify ingredient information (name, quantity, unit, expiration date, storage location)

### 🔄 Automated Notifications
- **Daily Check**: Automatically check for expiring ingredients
- **LINE Notifications**: Send reminders via LINE Messaging API
- **n8n Integration**: Support n8n workflow automation

### 📊 Data Storage
- **Google Sheets**: All ingredient data stored in Google Sheets
- **Real-time Sync**: Local cache synchronized with cloud data
- **Backup Security**: Data automatically backed up to Google Drive

## 🛠️ Technical Architecture

- **AI Agent**: LangChain Agent system
- **LLM**: OpenAI GPT-4o-mini
- **Framework**: FastAPI + LINE Bot SDK
- **Storage**: Google Sheets API
- **Automation**: n8n workflows
- **Notifications**: LINE Messaging API

## 📦 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables Setup
Create `.env` file:
```env
# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# LINE Bot
LINE_CHANNEL_SECRET=your_line_channel_secret_here
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token_here

# Google Sheets
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
GOOGLE_SHEET_NAME=your_sheet_name
GOOGLE_WORKSHEET_NAME=ingredients
```

### 3. Setup Google Sheets
Refer to [Google Sheets Setup Guide](GOOGLE_SHEETS_SETUP.md)

### 4. Start Service
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 Usage

### LINE Bot Commands
- `ping` - Test connection
- `help` or `幫助` - Show help information
- `tools` or `工具` - Show available tools list

### Natural Language Commands
```
View ingredient inventory
Add milk 500ml expires tomorrow store in refrigerator
Check expiring ingredients
Reduce apples by 2
Delete expired bananas
Update milk quantity to 1000ml
```

## 🔧 Available Tools

### Ingredient Management Tools
- `add_ingredient` - Add ingredients to inventory
- `get_ingredient_list` - Get ingredient inventory list
- `check_expiring_ingredients` - Check ingredients expiring soon
- `delete_ingredient` - Completely delete ingredient items
- `reduce_ingredient_quantity` - Reduce ingredient quantity
- `update_ingredient` - Modify ingredient information

## 🔄 Automation Setup

### n8n Workflows
Set up daily automatic checks for expiring ingredients and send notifications:

1. **Reference Guide**: [n8n Setup Guide](N8N_SETUP_GUIDE.md)
2. **LINE Notifications**: [LINE Messaging API Setup](LINE_MESSAGING_API_SETUP.md)
3. **Configuration Example**: `n8n_line_config_example.json`

### API Endpoints
- `GET /api/expiring-ingredients` - Get expiring ingredients (for n8n calls)

## 🛠️ Helper Tools

### Get LINE User ID
```bash
python3 get_user_id.py
```
Send any message to your LINE Bot, and the tool will display your User ID.

## 📁 Project Structure

```
food-agent/
├── app.py                          # FastAPI main application
├── agent.py                        # AI Agent core logic
├── tools.py                        # Tool function collection
├── parser_chain.py                 # Text parser
├── google_sheets_storage.py        # Google Sheets integration
├── get_user_id.py                  # LINE User ID retrieval tool
├── requirements.txt                # Dependencies
├── .env                           # Environment variables (not committed)
├── .gitignore                     # Git ignore file
├── GOOGLE_SHEETS_SETUP.md         # Google Sheets setup guide
├── LINE_MESSAGING_API_SETUP.md    # LINE Messaging API setup guide
├── N8N_SETUP_GUIDE.md             # n8n workflow setup guide
├── n8n_line_config_example.json   # n8n configuration example
├── TECHNOLOGY_STACK.md            # Technical architecture documentation
├── README.md                      # Project description (Chinese)
├── README_EN.md                   # Project description (English)
└── TECHNOLOGY_STACK_EN.md         # Technical documentation (English)
```

## 🧪 Testing

### Test AI Agent
```bash
python3 test_agent.py
```

### Test Google Sheets Integration
```bash
python3 test_google_sheets.py
```

## 📝 Logging

The system automatically records detailed processing:
- User input and parsing
- Agent thinking process
- Tool call results
- Google Sheets operations
- Error handling

Log file: `food_agent.log`

## 🔒 Security Notes

1. **Environment Variables**: Don't hardcode sensitive information in code
2. **Google Sheets**: Regularly check service account permissions
3. **LINE API**: Regularly update Access Tokens
4. **Data Backup**: Regularly backup Google Sheets data

## 🚨 Important Reminders

- **LINE Notify Discontinuation**: LINE Notify service will be discontinued on March 31, 2025, please use LINE Messaging API
- **Date Processing**: System automatically uses current date (2025) for ingredient expiration dates
- **Free Quota**: LINE Messaging API has 500 free messages per month

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License

---

## 📚 Technical Documentation

### English Version
- **[Technical Architecture Documentation](TECHNOLOGY_STACK_EN.md)** - Detailed technical stack and architecture design
- **[Google Sheets Setup Guide](GOOGLE_SHEETS_SETUP.md)** - Google Sheets integration setup
- **[LINE Messaging API Setup Guide](LINE_MESSAGING_API_SETUP.md)** - LINE notification setup
- **[n8n Workflow Setup Guide](N8N_SETUP_GUIDE.md)** - Automation workflow setup

### 中文版 (Chinese Version)
- **[README (中文)](README.md)** - 專案說明 (中文版)
- **[技術架構文檔 (中文)](TECHNOLOGY_STACK.md)** - 技術文檔 (中文版)

## 📞 Support

If you encounter issues, please check:
1. Environment variables are correctly set
2. Google Sheets permissions are correct
3. LINE Bot configuration is complete
4. Check log files for detailed error information
5. Refer to technical documentation for detailed architecture
