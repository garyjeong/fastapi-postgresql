from enum import StrEnum
import os
from typing import Optional
from sqlalchemy import URL, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sshtunnel import SSHTunnelForwarder
from dotenv import load_dotenv

Base = declarative_base()


class AppEnv(StrEnum):
    LOCAL = "local"
    PRODUCTION = "production"


def load_env(env: AppEnv = AppEnv.LOCAL) -> None:
    """
    지정된 환경에 맞는 .env 파일을 로드합니다.
    """
    env_path = f"src/databases/envs/.env.{env}"
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Environment file not found: {env_path}")

    load_dotenv(env_path)
    os.environ["ENV"] = env


def create_tunnel() -> Optional[SSHTunnelForwarder]:
    """
    운영 환경인 경우 SSH 터널을 생성합니다.
    """
    if os.getenv("ENV") == AppEnv.LOCAL:
        return None

    required_env_vars = [
        "SSH_HOST",
        "SSH_PORT",
        "SSH_USER",
        "SSH_KEY_PATH",
        "DATABASE_HOST",
        "DATABASE_PORT",
    ]

    # 필요한 환경 변수가 모두 있는지 확인
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    return SSHTunnelForwarder(
        (os.getenv("SSH_HOST"), int(os.getenv("SSH_PORT", 22))),
        ssh_username=os.getenv("SSH_USER"),
        ssh_pkey=os.getenv("SSH_KEY_PATH"),
        remote_bind_address=(
            os.getenv("DATABASE_HOST"),
            int(os.getenv("DATABASE_PORT", 5432)),
        ),
    )


def get_database_url(tunnel: Optional[SSHTunnelForwarder] = None) -> URL:
    """
    환경에 맞는 데이터베이스 URL을 생성합니다.
    """
    required_env_vars = ["DATABASE_USER", "DATABASE_PASSWORD", "DATABASE_NAME"]

    # 필요한 환경 변수가 모두 있는지 확인
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    # 터널이 있으면 localhost와 터널 포트 사용
    if tunnel:
        host = "localhost"
        port = tunnel.local_bind_port
    else:
        host = os.getenv("DATABASE_HOST", "localhost")
        port = int(os.getenv("DATABASE_PORT", 5432))

    return URL.create(
        drivername="postgresql",
        username=os.getenv("DATABASE_USER"),
        password=os.getenv("DATABASE_PASSWORD"),
        host=host,
        port=port,
        database=os.getenv("DATABASE_NAME"),
    )


def create_engine_with_tunnel(env: AppEnv = AppEnv.LOCAL) -> Engine:
    """
    지정된 환경에 맞는 데이터베이스 엔진을 생성합니다.
    """
    # 환경 변수 로드
    load_env(env)

    # SSH 터널 생성 (필요한 경우)
    tunnel = create_tunnel()
    if tunnel:
        tunnel.start()

    # 데이터베이스 URL 생성 및 엔진 반환
    url = get_database_url(tunnel)
    return create_engine(url)
