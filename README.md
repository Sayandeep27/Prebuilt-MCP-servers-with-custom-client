# 🌦️➕🧮 MCP Multi‑Server Setup (Weather + Calculator)

A clean, end‑to‑end guide to running **multiple public MCP servers locally** and connecting them to **one LangChain/LangGraph client**.

This README walks you through:

* What MCP servers are
* How to run **Weather MCP (Go)**
* How to run **Calculator MCP (Python)**
* How your **client talks to both servers at once**

---

## 🧠 What is MCP (Model Context Protocol)?

**MCP** lets tools run as **independent servers** that LLMs can call dynamically.

Instead of:

* Writing tool logic inside your app

You:

* Run tools as servers
* Let LLMs discover and call them

This gives you:

* Tool reuse
* Language‑agnostic servers
* Agent‑friendly architecture

---

## 📚 Public MCP Servers

Official list of community MCP servers:

🔗 [https://github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

We’ll use two:

| Server         | Language | Purpose                         |
| -------------- | -------- | ------------------------------- |
| Weather MCP    | Go       | Weather data via OpenWeatherMap |
| Calculator MCP | Python   | Math operations                 |

---

## 🌦️ Weather MCP Server (Go)

### Step 1 — Install Go

Download and install Go:

🔗 [https://go.dev/dl/](https://go.dev/dl/)

Verify installation:

```bash
go version
```

---

### Step 2 — Clone & Build Weather MCP

```bash
git clone https://github.com/mschneider82/mcp-openweather.git
cd mcp-openweather
go build -o mcp-weather
```

This creates a binary called **mcp-weather**.

---

### Step 3 — Get OpenWeatherMap API Key

1. Visit [https://openweathermap.org/api](https://openweathermap.org/api)
2. Create a free account
3. Copy your API key (**appid**)
4. Wait a few hours if it doesn’t work immediately

Set the environment variable:

```bash
export OPENWEATHER_API_KEY=your_api_key
```

(Windows PowerShell)

```powershell
$env:OPENWEATHER_API_KEY="your_api_key"
```

---

### Step 4 — Run Weather MCP Server

```bash
./mcp-weather
```

⚠️ **Keep this terminal running** — this is your MCP server.

---

## 🧮 Calculator MCP Server (Python)

### Step 1 — Install Calculator Server

```bash
pip install mcp-server-calculator
```

---

### Step 2 — Run Calculator MCP

```bash
python -m mcp_server_calculator
```

⚠️ Keep this terminal running as well.

---

## 🧑‍💻 MCP Client Setup (LangChain + LangGraph)

### Install Client Dependencies

```bash
pip install python-dotenv langchain-mcp-adapters langgraph "langchain[openai]" mcp
```

---

### What the Client Does

Your **mcp_client.py**:

* Connects to **multiple MCP servers**
* Registers all tools
* Lets the LLM decide:

  * When to call weather
  * When to call calculator

All from **one prompt**.

---

## 🖥️ Terminal Layout (Very Important)

You must run **three terminals**:

### Terminal 1 — Weather MCP

```bash
./mcp-weather
```

---

### Terminal 2 — Calculator MCP

```bash
python -m mcp_server_calculator
```

---

### Terminal 3 — Client

```bash
python mcp_client.py
```

---

## 🔁 How Everything Talks

````
User Prompt
   ↓
LangChain / LangGraph Client
   ↓
MultiServerMCPClient
   ↓
┌───────────────┬────────────────┐
│ Weather MCP   │ Calculator MCP │
│ (Go Server)   │ (Python Server)│
└───────────────┴────────────────┘n```

The LLM **chooses tools automatically**.

---

## ✨ Why This Architecture is Powerful

- Tools can be written in **any language**
- Servers can live on **any machine**
- Clients can be **agents, UIs, or pipelines**
- Perfect for **agent systems & A2A**

---

## 🚀 Next Ideas

- Add more MCP servers (Search, DB, Files)
- Wrap client with Streamlit UI
- Connect multiple agents
- Use MCP with A2A orchestration

---

## ✅ Summary

You now have:

- A Go‑based Weather MCP server
- A Python‑based Calculator MCP server
- One LangChain client using both
- A real **multi‑tool agent system**

This is **production‑grade agent architecture**.

Happy building 🧠⚡

````
