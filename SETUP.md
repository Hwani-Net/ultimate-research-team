# 🛸 Antigravity Ultimate Research Team - Setup Guide
## Complete Environment Setup for Any Computer

---

## 📋 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)
- **Python**: 3.10 or higher (3.11+ recommended)
- **RAM**: 4GB minimum (8GB+ recommended)
- **Disk Space**: 500MB for dependencies

### Recommended Setup
- **Python**: 3.11.7 or 3.12.x
- **RAM**: 16GB
- **Internet**: Stable connection for AI API calls

---

## 🚀 Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Hwani-Net/ultimate-research-team.git
cd ultimate_research_team
```

### 2. Set Up Python Environment

#### Option A: Using venv (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows (PowerShell):
.\\venv\\Scripts\\Activate.ps1
# Windows (Command Prompt):
venv\\Scripts\\activate.bat
# macOS/Linux:
source venv/bin/activate
```

#### Option B: Using conda
```bash
conda create -n antigravity python=3.11
conda activate antigravity
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected packages installed:**
- `streamlit` - Web UI framework
- `crewai[tools]` - Multi-agent orchestration
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation
- And other dependencies...

### 4. Configure API Keys

#### Step 4.1: Copy Environment Template
```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS/Linux
cp .env.example .env
```

#### Step 4.2: Get Your API Keys

**Required Keys:**

1. **Google Gemini API** (Free tier available)
   - Visit: https://makersuite.google.com/app/apikey
   - Click "Get API Key" → "Create API key in new project"
   - Copy key to `GOOGLE_API_KEY` in `.env`

2. **Tavily Search API** (Free: 1000 searches/month)
   - Visit: https://tavily.com
   - Sign up and get API key
   - Copy key to `TAVILY_API_KEY` in `.env`

**Optional Keys (for advanced models):**

3. **OpenAI API** (for GPT-4o, GPT-5)
   - Visit: https://platform.openai.com/api-keys
   - Copy key to `OPENAI_API_KEY` in `.env`

4. **Anthropic Claude API** (for Claude 3.5, 4.0)
   - Visit: https://console.anthropic.com/
   - Copy key to `ANTHROPIC_API_KEY` in `.env`

#### Step 4.3: Edit .env File
Open `.env` in any text editor and replace placeholder values:
```env
GOOGLE_API_KEY=your_actual_google_key_here
TAVILY_API_KEY=your_actual_tavily_key_here
OPENAI_API_KEY=your_actual_openai_key_here
ANTHROPIC_API_KEY=your_actual_anthropic_key_here
```

### 5. Verify Installation
```bash
python verify_v11_1.py
```

**Expected output:**
```
✅ All agents configured correctly
✅ API keys loaded
✅ System ready
```

---

## 🎮 Running the Application

### Local Development (Streamlit UI)
```bash
streamlit run app.py
```

**Access at:** http://localhost:8501

### Command-Line Simulation
```bash
python simulate_interaction.py
```

### Board Consultation (Emergency)
```bash
python board_consultation_kill_switch.py
```

---

## 🐳 Docker Setup (Alternative)

### Build Image
```bash
docker build -t antigravity-research .
```

### Run Container
```bash
docker run -p 8501:8501 --env-file .env antigravity-research
```

**Note:** Docker setup requires `Dockerfile` (to be created if needed)

---

## 🔧 Troubleshooting

### Issue 1: "Module not found"
**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Issue 2: "API Key Invalid"
**Solution:**
1. Check `.env` file has correct keys (no quotes, no spaces)
2. Regenerate keys from provider dashboards
3. Restart Python/terminal after editing `.env`

### Issue 3: "Permission Denied" (Windows)
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 4: Port 8501 Already in Use
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

---

## 📂 Project Structure

```
ultimate_research_team/
├── app.py                      # Main Streamlit Application
├── agents.py                   # AI Agent Definitions (SOTA Models)
├── tasks.py                    # Task Definitions (Kill Switch, Board, Execution)
├── models.py                   # Pydantic Models for Structured Output
├── simulate_interaction.py     # CLI Simulation Tool
├── verify_v11_1.py            # System Health Check
├── requirements.txt           # Python Dependencies
├── .env.example               # Environment Template
├── .env                       # [YOU CREATE] Your API Keys
├── ANTIGRAVITY_MASTER_MANUAL.md # Core Operating Philosophy
├── blueprint.md               # Current Project Blueprint
├── 작업.md                     # Work Log (Korean)
└── README.md                  # This file
```

---

## 🌐 Environment Variables Reference

| Variable | Required | Purpose | Get From |
|----------|----------|---------|----------|
| `GOOGLE_API_KEY` | ✅ Yes | Gemini AI Models | https://makersuite.google.com |
| `TAVILY_API_KEY` | ✅ Yes | Web Search | https://tavily.com |
| `OPENAI_API_KEY` | ⚠️ Optional* | GPT Models | https://platform.openai.com |
| `ANTHROPIC_API_KEY` | ⚠️ Optional | Claude Models | https://console.anthropic.com |

*May be required by CrewAI even when using Gemini (set dummy value if needed)

---

## 📖 Usage Guide

### Quick Start
1. Launch app: `streamlit run app.py`
2. Select research mode (3-Agent Speed / 5-Agent Deep)
3. Enter topic or use templates
4. Click "바로 연구 시작" (Start Research)

### Advanced Features
- **Magic Prompt Upgrade**: AI refines your prompt
- **Board Governance**: Strategic validation before execution
- **Kill Switch**: Filters out doomed projects automatically
- **A/B Testing**: Compare 3-agent vs 5-agent results

**Full documentation:** See `USAGE_GUIDE.md`

---

## 🔐 Security Best Practices

1. **Never commit `.env`** (already in `.gitignore`)
2. **Rotate API keys** if exposed
3. **Use `.env.local`** for local overrides (add to `.gitignore`)
4. **Set rate limits** on API dashboards to prevent overage

---

## 🆘 Support

- **Issues**: https://github.com/Hwani-Net/ultimate-research-team/issues
- **Discussions**: Use GitHub Discussions
- **Documentation**: See `ANTIGRAVITY_MASTER_MANUAL.md`

---

## 📜 License

See `LICENSE` file

---

**System Version:** v11.5.1 (Board Governance Update)  
**Last Updated:** 2026-02-09  
**Maintainer:** Antigravity AI (Soulless Mode)
