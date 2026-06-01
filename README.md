# 🧠 Research Mind


![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![LangChain](https://img.shields.io/badge/LangChain-Framework-green)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20AI-orange)
![Google Gemini](https://img.shields.io/badge/Google-Gemini-blue?logo=google)
![Mistral AI](https://img.shields.io/badge/Mistral-AI-purple)
![Tavily](https://img.shields.io/badge/Tavily-Search-black)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)
![Contributions](https://img.shields.io/badge/Contributions-Welcome-brightgreen)


Research Mind is an AI-powered multi-agent research assistant that automates the complete research workflow. It searches the web, extracts information from sources, generates structured research reports, and evaluates report quality using multiple AI agents.

## ✨ Features

* 🔍 **Search Agent**

  * Finds relevant and recent information from the web using Tavily Search.

* 📖 **Reader Agent**

  * Scrapes and extracts content from selected sources.

* ✍️ **Writer Chain**

  * Generates detailed and structured research reports.

* 🔬 **Critic Chain**

  * Reviews generated reports and provides quality scores and feedback.

* 📊 **Interactive Dashboard**

  * Modern Streamlit interface with progress tracking and research history.

* 📁 **Export Reports**

  * Download generated reports as text files.

---

## 🏗️ Architecture

```text
User Query
     │
     ▼
┌──────────────┐
│ Search Agent │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Reader Agent │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Writer Chain │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Critic Chain │
└──────┬───────┘
       │
       ▼
 Final Research Report
```

---

## 🚀 Tech Stack

### Frontend

* Streamlit

### AI Frameworks

* LangChain
* LangGraph

### Search & Research

* Tavily Search API
* BeautifulSoup
* Requests

### LLM Integration

* Google Gemini
* Mistral-ai

### Utilities

* Python Dotenv

---

## 📂 Project Structure

```text
research-mind/
│
├── app.py
├── pipeline.py
├── agents.py
├── requirements.txt
├── README.md
├── .gitignore

```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/someshvermagithub/multi-agent-research-assistant.git
cd research-mind
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows:

```bash
.venv\Scripts\activate
```

Linux/Mac:

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
MISRAL_API_KEY=your_mistral_api_key
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

The application will open in your browser at:

http://localhost:8501

---

## 📸 Example Research Topics

* Artificial General Intelligence
* Quantum Computing in 2025
* CRISPR Gene Editing
* Climate Technology Innovations
* Neuralink Progress
* Future of Autonomous AI Agents

---
## 🚀 Live Application

Experience Research Mind directly in your browser:

🔗 **Live Demo:** https://multi-agent-full-research-assistant.streamlit.app/

[![Open Research Mind](https://img.shields.io/badge/Launch-Research%20Mind-ff4b4b?logo=streamlit&logoColor=white)](https://multi-agent-full-research-assistant.streamlit.app/)

No installation required. Simply open the application, enter a research topic, and let the AI-powered multi-agent system search, analyze, write, and critique a comprehensive research report.

---
## 📊 Workflow

1. User enters a research topic.
2. Search Agent gathers relevant sources.
3. Reader Agent extracts content from selected URLs.
4. Writer Chain generates a comprehensive report.
5. Critic Chain evaluates the report quality.
6. Results are displayed and can be downloaded.

---

## 🌟 Future Improvements

* PDF report export
* Citation generation
* Multi-language research support
* Research report sharing
* Voice-based research queries
* Persistent database storage
* Agent performance analytics

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

![AI](https://img.shields.io/badge/AI-Powered-purple)
![Multi-Agent](https://img.shields.io/badge/Multi-Agent_System-blueviolet)
![Research](https://img.shields.io/badge/Research-Automation-cyan)
![Made With Love](https://img.shields.io/badge/Made%20with-❤️-red)

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Somesh Verma

Passionate about AI Agents, LLM Applications, Machine Learning, and Full Stack Development.

## 📈 GitHub Stats


