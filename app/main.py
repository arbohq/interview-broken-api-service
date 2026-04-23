import logging
import logging.config
from pathlib import Path

from fastapi import FastAPI, HTTPException

from app.models import CategorizeRequest, CategorizationResult
from app.parser import parse_llm_output

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "service.log",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console", "file"],
    },
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

app = FastAPI(title="Interview - Broken API Service")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/categorize", response_model=CategorizationResult)
def categorize(payload: CategorizeRequest) -> CategorizationResult:
    try:
        result = parse_llm_output(
            llm_output=payload.llm_output,
            allowed_categories=payload.categories,
        )
        logger.info("Categorization result: %s", result.suggested_category)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected error while categorizing")
        raise HTTPException(status_code=500, detail="Internal server error") from exc

