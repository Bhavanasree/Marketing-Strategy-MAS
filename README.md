# BrandForge AI

BrandForge AI is a marketing assistant project that combines Streamlit, Supabase authentication/storage, Amazon Bedrock AI, and a modular agent toolchain to generate marketing strategy, brand ideas, logos, SEO, email campaigns, ad copy, and social media content.

## Key Features

- Streamlit web app with user authentication via Supabase
- Conversational marketing assistant powered by LangGraph and Amazon Bedrock
- Logo generation using Amazon Titan Image Generator
- Marketing strategy planning, SEO keywords, ad copy, email campaign drafts, social media content, and domain suggestions
- Conversation persistence with Supabase database storage
- PDF export for generated marketing plans
- CLI interface for basic agent conversation

## Project Structure

- `app.py` - Main Streamlit web application entrypoint
- `auth.py` - Supabase authentication helpers for sign-up, sign-in, and sign-out
- `db.py` - Supabase persistence helpers for conversations and messages
- `cli.py` - Command-line interface for interacting with the marketing agent
- `supabase_client.py` - Supabase client initialization
- `storage.py` - (if used) application storage helper module
- `agents/` - tool definitions for marketing tasks
  - `ad_copy_agent.py`
  - `domain_agent.py`
  - `email_campaign_agent.py`
  - `logo_agent.py`
  - `seo_agent.py`
  - `social_media_agent.py`
  - `strategy_agent.py`
  - `tagline_agent.py`
- `graph/` - LangGraph-based agent orchestration
  - `graph.py` - graph builder and agent orchestration
  - `prompt.py` - system prompt and assistant behavior rules
  - `state.py` - agent state definitions
- `utils/` - helper utilities
  - `pdf_generator.py` - generates a marketing plan PDF
  - `title_generator.py` - creates short titles for prompts and history
- `generated_logos/` - generated logo output directory
- `marketing_plan.pdf` - sample or generated marketing plan output

## Getting Started

### Prerequisites

- Python 3.11+ recommended
- A Supabase project with authentication and tables for `conversations` and `messages`
- AWS credentials configured for Bedrock access
- `.env` file with Supabase and AWS settings

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root with the following values:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_DEFAULT_REGION=us-east-1
```

> If you are using Amazon Bedrock, ensure the Bedrock client is configured for your AWS environment.

### Supabase Tables

The app expects a Supabase schema with at least these tables:

- `conversations`
  - `id`
  - `user_id`
  - `title`
  - `created_at`
- `messages`
  - `id`
  - `conversation_id`
  - `role`
  - `content`
  - `created_at`

## Running the Application

### Streamlit Web App

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (typically `http://localhost:8501`).

### CLI Mode

```bash
python cli.py
```

The CLI provides a simple conversational interface using the same agent graph.

## How It Works

1. `app.py` initializes Streamlit UI and manages page state.
2. User auth is handled by `auth.py` using Supabase.
3. Conversations and chat history are saved through `db.py`.
4. The `graph/` directory defines the LangGraph state machine and prompt rules.
5. `agents/__init__.py` exposes a toolset used by the AI agent.
6. `logo_agent.py` generates logos via Amazon Titan and saves them in `generated_logos/`.
7. `utils/pdf_generator.py` can export marketing plan text to PDF.

## Usage Notes

- The app is designed as a marketing consultant assistant, guiding users through branding and strategy.
- Generated logos are stored locally in `generated_logos/`.
- PDF export uses `reportlab` to create a simple marketing report.
- The `prompt.py` file contains the assistant behavior rules and tool usage instructions.

## Optional Improvements

- Add input validation and stronger session security
- Add richer UI sections for specific marketing outputs
- Add more tool-specific prompts and richer formatting
- Add database migration scripts for Supabase schema

## Dependencies

The project depends on packages listed in `requirements.txt`, including:

- `streamlit`
- `langchain-core`
- `langchain-aws`
- `langgraph`
- `python-dotenv`
- `boto3`
- `supabase`
- `reportLab`

## Notes

- `app.py` currently includes a landing page, auth pages, and internal agent view logic.
- `supabase_client.py` loads environment variables and creates the Supabase client.
- `graph/graph.py` binds tools to an LLM and builds the state graph for the AI agent.

---