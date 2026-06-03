# Doc D AI Engine

The Doc D AI Engine is the core intelligence framework behind the Viligans Command ecosystem.  
It powers automation, compliance assistance, rural infrastructure tools, and modular AI agents designed to support veterans, small businesses, and trust‑based operations.

---

## 🚀 Features

- Modular AI agent architecture  
- Compliance and procedural reasoning engine  
- Document parsing and structured output generation  
- Rural infrastructure + NEMT automation modules  
- Trust‑based logic layer (RIET → VCC → Subsidiaries)  
- Extensible plugin system for future tools

## 🧱 Project Structure

```
/src
  /core
  /agents
  /pipelines
  /parsers
  /services
  /utils

/docs
/tests
/config
```

## 🛠 Tech Stack 

- Python or Node.js  
- FastAPI / Express  
- Vector DB (Chroma / Pinecone)  
- Lightweight rules engine  
- GitHub Actions for CI/CD

## 📦 Installation & Run

```bash
git clone https://github.com/alawndus/docd-ai.git
cd docd-ai
```

Copy the example environment and start the app (Linux/macOS):

```bash
cp .env.example .env
./scripts/run.sh
```

On Windows PowerShell:

```powershell
copy .env.example .env
.\scripts\run.ps1
```

You can also use the Makefile shortcuts:

```bash
make build      # create venv and install deps
make run        # run uvicorn locally
make docker-build
make docker-run
```

## 🧪 Testing

```bash
pytest
```

## 📜 License

MIT License (see LICENSE file)

## 🤝 Contributing

Pull requests welcome.  
For major changes, open an issue first to discuss what you’d like to modify.

## 🛡 Maintainer

Alawndus L. Davis  
Viligans Command Corporation  
DOC D AI — Sentinel Intelligence Framework




  



