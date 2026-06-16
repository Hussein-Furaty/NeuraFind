# NeuraFind

**NeuraFind** is an offline Windows desktop application for semantic document search.
It helps users search inside local documents by meaning, not only by file names or exact keywords.

<p align="center">
  <img src="assets/neurafind-logo.png" alt="NeuraFind Logo" width="140"/>
</p>

---

## Overview

NeuraFind is designed as a local-first document intelligence workspace for Windows.
It indexes supported documents, extracts their textual content, generates local semantic representations, and allows users to search across their files using exact, fuzzy, semantic, and hybrid search methods.

The application is built with privacy in mind. Documents are processed locally, and search runs on the user's machine without sending file contents to external services.

---

## Screenshots

> Screenshots will be added after building the Windows executable.

### Main Interface

![Main Interface](docs/screenshots/home.png)

### Search Results

![Search Results](docs/screenshots/search-results.png)

### Preview Panel

![Preview Panel](docs/screenshots/preview-panel.png)

### Model Management

![Model Management](docs/screenshots/models-page.png)

### Settings

![Settings](docs/screenshots/settings-page.png)

---

## Key Features

* Offline-first semantic document search
* Local indexing of user-selected folders
* Exact search
* Fuzzy search
* Semantic search using local embedding models
* Hybrid search combining multiple search strategies
* Support for PDF, DOCX, XLSX, and PPTX files
* IDE-style desktop interface
* File explorer sidebar
* Search result preview
* Open file, open folder, and copy path actions
* Local AI model management
* Light and dark interface themes
* No cloud dependency for indexed documents

---

## Supported File Types

| Format | Status    |
| ------ | --------- |
| PDF    | Supported |
| DOCX   | Supported |
| XLSX   | Supported |
| PPTX   | Supported |

---

## Search Methods

NeuraFind currently supports four search modes:

| Search Type     | Description                                                                  |
| --------------- | ---------------------------------------------------------------------------- |
| Exact Search    | Matches exact words or phrases inside indexed documents.                     |
| Fuzzy Search    | Finds approximate matches even when the query contains spelling differences. |
| Semantic Search | Retrieves documents based on meaning using local embeddings.                 |
| Hybrid Search   | Combines exact, fuzzy, and semantic search results.                          |

---

## Local AI Models

NeuraFind uses local embedding models for semantic search.

Current supported model options:

| Model                                                         | Purpose                                    |
| ------------------------------------------------------------- | ------------------------------------------ |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Fast multilingual semantic search          |
| `intfloat/multilingual-e5-base`                               | More accurate multilingual semantic search |

Models are downloaded only when the user chooses to download them.
After download, semantic search runs locally.

---

## Architecture

The project follows a modular architecture:

```text
src/
└── neurafind/
    ├── embeddings/
    ├── indexing/
    ├── parsers/
    ├── search/
    ├── services/
    ├── storage/
    └── ui/
```

Main pipeline:

```text
Folder
→ File Scanner
→ Parser Manager
→ Document Parsers
→ Indexer
→ SQLite Storage
→ Embedding Storage
→ Hybrid Search
→ User Interface
```

More details are available in:

* `docs/architecture.md`
* `docs/requirements.md`
* `docs/tech-stack.md`

---

## Installation for Development

Clone the repository:

```bash
git clone https://github.com/Hussein-Furaty/NeuraFind.git
cd NeuraFind
```

Install dependencies:

```bash
py -3.11 -m pip install -r requirements.txt
```

Run the application:

```bash
$env:PYTHONPATH="."
py -3.11 src\neurafind\app.py
```

---

## Project Status

NeuraFind is currently in active development.

Completed:

* Document parsing
* File indexing
* SQLite document storage
* Vector storage
* Exact search
* Fuzzy search
* Semantic search
* Hybrid search
* Local model management
* Modern desktop UI

Planned:

* Windows executable build
* Improved packaging
* More complete documentation
* Screenshots and demo video
* Release version
* OCR support in future versions

---

## Roadmap

### v0.1.0-alpha

* Core indexing pipeline
* Local storage
* Exact, fuzzy, semantic, and hybrid search
* Windows desktop interface
* Local model management

### Future Work

* OCR support
* TXT and Markdown support
* Advanced preview engine
* Search benchmarking
* Installer or portable Windows release
* Performance optimization
* FAISS-based vector indexing

---

## Privacy

NeuraFind is designed to be local-first.

* Files are indexed locally.
* Search runs locally.
* Document contents are not uploaded to external services.
* AI models run on the user's machine after download.

---

## Author

**Hussein Al-Furati**
Cybersecurity student, software developer, and AI practitioner.

Email: `hussein.a.habeeb.sec@gmail.com`

GitHub: `Hussein-Furaty`

---

## Open Source


---

## License

