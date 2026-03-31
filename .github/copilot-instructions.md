# GitHub Copilot Instructions

This repository is a Streamlit-based marketing assistant project named BrandForge AI. It uses Supabase for authentication and persistence, Amazon Bedrock/Titan for AI and logo generation, and a LangGraph-based toolchain for marketing tasks.

## Repository Goals

- Provide a web UI for authenticated users to generate marketing strategy, branding assets, SEO recommendations, ad copy, email campaigns, and social media content.
- Persist conversations and generated outputs using Supabase.
- Generate marketing plan PDFs and logo assets.
- Support a simple CLI interface for agent interaction.
- Add marketing performance tooling such as KPI calculators and dashboard metrics.

## Helpful Guidance for Copilot

When suggesting code or completing files:

- Prioritize clean, modular code with clearly separated concerns.
- Use `type hints` for all functions and method signatures.
- Keep Streamlit UI logic in `app.py` and utility/helper logic in `utils/`.
- Add new dashboard features or KPI calculations by creating reusable helper functions and service modules, not by crowding `app.py`.
- Prefer explicit imports and avoid pulling in unrelated packages.
- Make sure new features fit naturally into the existing project structure.


## Project Structure Guidance

- `app.py` should handle Streamlit page layout, session state, and dashboard rendering.
- `auth.py` should handle Supabase authentication flows.
- `db.py` should handle Supabase persistence for conversations and messages.
- `graph/` should contain the LangGraph state machine, prompt rules, and agent orchestration.
- `agents/` should contain tool functions used by the AI agent.
- `utils/` should contain reusable helper functions, such as KPI math and PDF generation.

## Notes

- The project uses `python-dotenv` for configuration and expects `.env` values for `SUPABASE_URL`, `SUPABASE_KEY`, and AWS credentials.
- Generated logos are stored in `generated_logos/`.
- `requirements.txt` contains the primary dependencies.

If a change requires new functionality, keep the solution consistent with the current app structure and avoid mixing unrelated concerns.