# DevPulse Agent ⚡

DevPulse is an intelligent AI Developer & IT Support Assistant built with the Google Agent Development Kit (ADK) and deployed on Google Agent Platform. DevPulse assists software engineers, DevOps teams, and IT operators by managing support tickets, inspecting repositories, retrieving grounded documentation, executing sandboxed diagnostics, and generating visual architecture assets.

![DevPulse Agent Demo](demo.gif)

---

## 🚀 Key Capabilities & Implemented Tools

The features below reflect the actual tools and services integrated in `app/agent.py` and `app/tools.py`:

### 🧠 Long-Term Memory & Context
- **Vertex AI Memory Bank:** Automatically persists session events and retrieves developer preferences, project context, and safety rules across conversations using `PreloadMemoryTool`, `LoadMemoryTool`, and `add_session_to_memory`.

### 🗄️ Database & Ticket Management
- **Google Cloud Firestore:** Real-time database integration for reading support tickets (`read_support_tickets`), creating support tickets (`create_or_update_support_ticket`), and updating ticket resolution state (`manage_support_ticket`).

### 🎨 Visual & Media Asset Generation
- **Gemini Architecture Image Generation:** Generates system topology diagrams and IT badges (`generate_system_asset_image`) using `gemini-3.1-flash-lite-image` in the `global` region, saving local Playground artifacts and uploading directly to public Google Cloud Storage.
- **Gemini Video Generation:** Generates short IT status videos and animations (`generate_system_asset_video`) using `gemini-omni-flash-preview` in the `global` region, saving local Playground artifacts and returning public Cloud Storage HTTPS URLs.

### 🔍 Grounded Retrieval (RAG)
- **Vertex AI RAG Corpus:** Grounded vector search over internal developer knowledge base documentation (`search_knowledge_base`) and Project Gutenberg document corpora (`consult_gutenberg_corpus`).

### 💻 Code Execution & Diagnostics
- **Agent Engine Sandbox Code Executor:** Runs Python code in a secure Vertex AI Agent Engine Sandbox (`AgentEngineSandboxCodeExecutor`).
- **Sandboxed Diagnostic Tool:** Local diagnostic calculation tool (`run_diagnostic_code`) for system troubleshooting.

### 🌐 Live Public APIs & Developer Tooling
- **PyPI Package Metadata:** Queries package release information and dependency metadata live from the PyPI JSON API (`fetch_pypi_package_info`).
- **Local Git Repository Inspector:** Inspects active Git repository working tree status, commit history, and diffs (`inspect_local_git_status` / `git_repository_inspector`).
- **System Topology:** Summarizes active infrastructure component layouts (`get_system_topology`).

### 🎨 Agent-to-User Interface (A2UI)
- **A2UI Schema Manager (v0.8):** Renders clean, structured card-based UI surfaces for chat clients, powered by `A2uiSchemaManager` and `a2ui_callback`.

---

## 🛠️ Google Cloud Services Integrated

| Service | Purpose |
| :--- | :--- |
| **Vertex AI Agent Engine (Agent Platform)** | Agent hosting, runtime orchestration, and sandbox execution |
| **Vertex AI Memory Bank** | Session persistence and long-term memory retrieval |
| **Google Cloud Firestore** | NoSQL document storage for IT support tickets |
| **Google Cloud Storage (GCS)** | Public asset storage for generated images and videos |
| **Vertex AI RAG Search** | Grounded vector search over document corpora |
| **Google GenAI Models** | `gemini-2.5-flash`, `gemini-3.1-flash-lite-image`, `gemini-omni-flash-preview` |

---

## 💻 Local Setup & Execution

### Prerequisites

- Python 3.11+
- Google Cloud SDK (`gcloud`) authenticated with Application Default Credentials (`gcloud auth application-default login`)

### Installation

1. Clone the repository and navigate into the project directory:
   ```bash
   cd devpulse-agent
   ```

2. Create a Python virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r app/requirements.txt
   pip install -r frontend/requirements.txt
   ```

### Running the Local Agent Server

Start the local ADK server:
```bash
adk api_server --host 127.0.0.1 --port 18080 --reload_agents --no-reload .
```

### Running the Web Chat Frontend

In a separate terminal, start the FastAPI proxy and chat interface:
```bash
cd frontend
export AGENT_ENGINE_RESOURCE_NAME="<YOUR_AGENT_ENGINE_RESOURCE_NAME>"
export AGENT_DIRECTORY="app"
python main.py
```

---

## 📄 License

Apache License 2.0
