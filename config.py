
from sqlalchemy.engine import URL, make_url
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def preparar_url_banco(database_url: str) -> str:
    """Normaliza a URL do PostgreSQL e habilita SSL para o Supabase."""
    if not database_url or not database_url.strip():
        raise RuntimeError("A variável DATABASE_URL não foi configurada.")

    url = make_url(database_url.strip())

    if url.drivername in {"postgres", "postgresql"}:
        url = url.set(drivername="postgresql+psycopg2")

    host = (url.host or "").lower()
    if url.drivername.startswith("postgresql") and (
        host.endswith(".supabase.co") or host.endswith(".pooler.supabase.com")
    ):
        query = dict(url.query)
        query.setdefault("sslmode", "require")
        url = url.set(query=query)

    return url.render_as_string(hide_password=False)


def opcoes_engine(database_url: str) -> dict:
    """Evita conexões inativas após pausas ou reciclagens do pool remoto."""
    url: URL = make_url(database_url)
    if url.drivername.startswith("sqlite"):
        return {}

    return {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }
