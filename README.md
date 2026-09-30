# AI Knowledge Assistant

An end-to-end AI application demonstrating **LLM + RAG + MCP** with a
clean engineering architecture.

## Overview

The assistant can answer:

1.  **Policy questions** using Retrieval-Augmented Generation (RAG).
2.  **Employee-specific questions** using MCP tools and employee data.
3.  **Combined questions** using both policy documents and employee
    information.

The project is intentionally implemented without LangChain so the
underlying LLM, RAG, tool-calling, and MCP concepts remain visible.

## Architecture

``` text
User
  |
  v
Streamlit UI
  |
  v
AI Orchestrator
  |--------------------|
  v                    v
RAG                  MCP
  |                    |
PDF -> Chunks ->       MCP Client
Embeddings ->          |
ChromaDB               v
  |                 MCP Server
  |                    |
  |                 Employee Data
  |                    |
  |---------|----------|
            v
           LLM
            |
            v
     Final Answer
     + Sources
     + Tools Used
```

## Project Structure

``` text
AI Knowledge Assistant/
├── app/
│   ├── main.py

│   ├── llm/
│   │   └── client.py
│   ├── rag/
│   │   ├── document_loader.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── rag_pipeline.py
│   │   └── generator.py
│   ├── mcp/
│   │   ├── server.py
│   │   └── client.py
│   ├── orchestrator.py
│   └── app.py
├── documents/
│   └── leave_policy_sample.pdf
├── chroma_db/
├── tests/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## RAG Pipeline

``` text
PDF
 |
 v
Document Loader
 |
 v
Text Extraction
 |
 v
Chunking
 |
 v
Embeddings
 |
 v
ChromaDB
```

At query time:

``` text
User Question
 |
 v
Query Embedding
 |
 v
ChromaDB Semantic Search
 |
 v
Top-K Chunks
 |
 v
Similarity Filtering
 |
 v
LLM Context
```

The current implementation uses simple character-based chunking with
approximately 500-character chunks and 50-character overlap.

Each chunk stores metadata such as:

``` python
{
    "source": "leave_policy_sample.pdf",
    "page": 1
}
```

The project uses `text-embedding-3-small` for both document and query
embeddings.

## MCP

The MCP server exposes employee tools such as:

``` text
get_employee
get_leave_balance
get_leave_history
```

Example:

``` python
await client.call_tool(
    "get_leave_balance",
    {"employee_id": "EMP001"}
)
```

Example result:

``` json
{
  "annual_leave": 12,
  "sick_leave": 8
}
```

The MCP client first discovers tools with `list_tools()`, then invokes
the required tool. The LLM does not directly access employee data.

## LLM + MCP Tool Calling

``` text
User Question
     |
     v
    LLM
     |
     | requests tool
     v
MCP Client
     |
     v
MCP Server
     |
     v
Employee Data
     |
     v
Tool Result
     |
     v
    LLM
     |
     v
Final Answer
```

This separates reasoning from enterprise data access.

## Orchestrator

The orchestrator is the central application layer. It is responsible
for:

-   Receiving the user question
-   Retrieving RAG context
-   Discovering MCP tools
-   Sending context and tools to the LLM
-   Detecting tool calls
-   Executing MCP tools
-   Sending tool results back to the LLM
-   Returning the final answer
-   Returning RAG sources and tools used

A consistent result contract is used:

``` python
{
    "answer": "...",
    "sources": [...],
    "tools_used": [...],
    "error": None
}
```

This keeps Streamlit independent from ChromaDB, embeddings, MCP
internals, and LLM orchestration.

## Streamlit UI

The UI is intentionally a thin presentation layer.

It handles:

-   User input
-   Employee ID
-   Conversation display
-   Loading state
-   Final answer
-   Sources
-   Tools used
-   User-facing errors

It should not contain RAG, MCP, or LLM business logic.

Run the application with:

``` powershell
.\.venv\Scripts\python.exe -m streamlit run app\ui\streamlit_app.py
```

## Configuration

Create `.env`:

``` env
OPENAI_API_KEY=your_api_key_here
```

Do not commit `.env` to Git.

Use `.env.example` for documenting required variables.

## Installation

Create a virtual environment:

``` powershell
python -m venv .venv
```

Activate it:

``` powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

``` powershell
pip install -r requirements.txt
```

## Sample Questions

### RAG

``` text
How many annual leave days are provided?
```

### MCP

``` text
What is my current leave balance?
My employee ID is EMP001.
```

### RAG + MCP

``` text
What is the carry-forward policy, and how many annual leave days do I currently have?
```

## Sample Policy Data

The sample PDF contains:

-   Annual Leave
-   Leave Application
-   Emergency Leave
-   Carry Forward
-   Public Holidays

Example values include:

``` text
Annual Leave: 20 days
Advance request: 5 working days
Carry forward: Up to 5 days
Manager approval: Required
```

These values are sample data for demonstrating the architecture.

## Engineering Principles

### Separation of concerns

``` text
UI
 |
 v
Orchestrator
 |
 +--> RAG
 |
 +--> MCP
 |
 +--> LLM
```

### Configuration

Secrets and environment-specific settings are kept outside application
code.

### Testability

Individual components can be tested independently:

-   Document loader
-   Chunker
-   Embedding service
-   Vector store
-   RAG retrieval
-   MCP tools
-   Orchestrator

### Observability

A production implementation should record:

-   Request ID
-   Retrieval latency
-   Number of retrieved chunks
-   Retrieval distance
-   Tools used
-   Tool latency
-   LLM latency
-   Errors

Sensitive employee information should not be written to logs.

## Security

The current project uses mock employee data and is intended for
learning.

A production system should add:

-   Authentication
-   Authorization
-   Employee-level access control
-   Secret management
-   Input validation
-   Tool permission policies
-   Confirmation for state-changing tools

A useful policy is:

``` text
Read-only tool
    |
    +--> automatic execution

State-changing tool
    |
    +--> require user confirmation
```

For example, `get_leave_balance()` can be read-only, while a future
`apply_leave()` operation should require confirmation.

## Current Limitations

-   Character-based chunking
-   Simple similarity threshold
-   Mock employee data
-   Limited MCP tools
-   One sample policy document
-   Basic conversation memory
-   Basic error handling
-   No authentication or authorization
-   No automated RAG evaluation
-   No production deployment
-   Streamlit directly calls the orchestrator

## Planned Improvements

### RAG

-   Semantic paragraph/sentence chunking
-   Metadata filtering
-   Hybrid search
-   Re-ranking
-   Retrieval evaluation
-   Citation validation

### MCP

-   More enterprise tools
-   REST API integration
-   Authentication
-   Authorization
-   Tool permission policies
-   Confirmation for write operations

### Engineering

-   Centralized configuration
-   Dedicated LLM client
-   Structured response models
-   Logging
-   Unit tests
-   Integration tests
-   Better exception handling

### Application Architecture

Move toward:

``` text
React / Streamlit
       |
       v
FastAPI
       |
       v
AI Orchestrator
       |
   +---+---+
   |       |
  RAG     MCP
   |       |
   +---+---+
       |
       v
      LLM
```

This allows the AI backend to serve multiple clients.

## Technologies

  Technology          Purpose
  ------------------- -------------------------------------------
  Python              Application development
  OpenAI LLM          Response generation and tool calling
  OpenAI Embeddings   Vector representation
  ChromaDB            Vector storage and semantic search
  MCP                 Tool integration and external data access
  Streamlit           User interface
  pypdf               PDF text extraction
  python-dotenv       Environment configuration

## Learning Outcomes

This project provides hands-on experience with:

-   Large Language Models
-   Prompt engineering
-   OpenAI Responses API
-   Function/tool calling
-   Embeddings
-   Vector databases
-   Semantic search
-   RAG
-   MCP architecture
-   MCP client/server communication
-   AI orchestration
-   Context management
-   Source attribution
-   Streamlit
-   Python application architecture
-   Error handling
-   Security
-   Observability

## Key Design Principle

> **The UI should not contain AI business logic.**

The intended flow is:

``` text
Streamlit
    |
    v
Orchestrator
    |
    +--> LLM
    +--> RAG
    +--> MCP
    |
    v
Structured Response
    |
    v
Streamlit
```

This separation makes the system easier to test, maintain, extend, and
eventually move from a prototype to a production AI service.

## Author

AI Knowledge Assistant --- LLM + RAG + MCP learning and portfolio
project.

Built as part of an AI Engineering learning journey, with emphasis on
understanding the underlying architecture before introducing
higher-level frameworks such as LangChain or LangGraph.
