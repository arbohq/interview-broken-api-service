# Broken API Service (Interview Exercise)

Github Link: https://github.com/arbohq/interview-broken-api-service

This is a small FastAPI service used for debugging and code-quality interviews.

## Candidate Task

You are given a service with known quality issues.
Your goal is to:

1. Run the API locally.
2. Diagnose and fix issues so the API starts reliably.
3. Improve parser correctness and error behavior.
4. Explain the fixes and tradeoffs.

## Run

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Use Python 3.11 or 3.12 for this exercise.

## Endpoint

`POST /categorize`

Example request:

```json
{
  "description": "AWS monthly bill",
  "categories": ["Software", "Travel", "Utilities"],
  "llm_output": "{\"suggested_category\":\"Software\",\"confidence_score\":0.88,\"reasoning\":\"Cloud services\"}"
}
```

Expected response shape:

```json
{
  "suggested_category": "Software",
  "confidence_score": 0.88,
  "reasoning": "Cloud services",
  "status": "success"
}
```

## What interviewers evaluate

- Debugging speed and root-cause analysis
- API reliability choices
- Parser robustness and safety
- Test strategy and communication
