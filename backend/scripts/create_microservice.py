import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "microservice"


def to_snake(name: str) -> str:
    name = name.replace("-", "_")
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return re.sub(r"_+", "_", name).lower().strip("_")


def to_pascal(name: str) -> str:
    return "".join(part.capitalize() for part in to_snake(name).split("_") if part)


def render(text: str, ctx: dict[str, str]) -> str:
    for k, v in ctx.items():
        text = text.replace(f"{{{{{k}}}}}", v)
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold a new FastAPI microservice with MVC structure")
    parser.add_argument("name", help="Service name, e.g. payment-service or payment")
    parser.add_argument("--port", default="8000")
    parser.add_argument("--db", action="store_true", help="Include SQLAlchemy db/model scaffolding")
    args = parser.parse_args()

    raw = args.name.strip()
    service_name = raw if raw.endswith("-service") else f"{raw}-service"
    snake = to_snake(service_name.replace("-service", ""))
    pascal = to_pascal(snake)
    target = ROOT / service_name
    if target.exists():
        raise SystemExit(f"Target already exists: {target}")

    ctx = {
        "service_name": service_name,
        "service_title": f"{pascal} Service",
        "entity_snake": snake,
        "entity_pascal": pascal,
        "entity_table": snake,
        "service_port": args.port,
    }

    for src in TEMPLATE.rglob("*"):
        rel = src.relative_to(TEMPLATE)
        dest = target / render(str(rel), ctx)
        if src.is_dir():
            dest.mkdir(parents=True, exist_ok=True)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        content = src.read_text()
        if not args.db and ("app/db/" in str(rel) or "app/models/" in str(rel)):
            continue
        dest.write_text(render(content, ctx))

    main_py = target / "app/main.py"
    if not args.db and main_py.exists():
        main_py.write_text(
            f"from fastapi import FastAPI\n\nfrom app.views.{snake} import router as {snake}_router\n\n"
            f"app = FastAPI(title=\"{pascal} Service\")\napp.include_router({snake}_router)\n\n\n"
            "@app.get('/health')\ndef health() -> dict[str, str]:\n    return {'status': 'ok'}\n"
        )
        req = target / "requirements.txt"
        req.write_text("fastapi==0.115.6\nuvicorn[standard]==0.32.1\npydantic==2.10.3\npydantic-settings==2.6.1\n")

    print(f"Created {target}")


if __name__ == "__main__":
    main()