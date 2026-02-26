# app/redis_cache.py
import json
import functools
from typing import Callable, Optional
from fastapi import Request
from app.redis_config import RedisConfig
from pydantic import BaseModel
from app.log_config.logging_config import get_logger

logger = get_logger(__name__)

def _serialize(data) -> str:
    """Converte o resultado para string JSON, suportando Pydantic e listas de Pydantic."""
    if isinstance(data, BaseModel):
        return data.model_dump_json()
    if isinstance(data, list) and all(isinstance(i, BaseModel) for i in data):
        return json.dumps([i.model_dump() for i in data])
    return json.dumps(data)

def redis_cache(ttl: int = 300, key_prefix: str = ""):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            redis = RedisConfig.get_instance()

            prefix = key_prefix or func.__name__
            key_params = ":".join(str(v) for v in kwargs.values() if not isinstance(v, Request))
            cache_key = f"{prefix}:{key_params}" if key_params else prefix

            try:
                cached = redis.get(cache_key)
                if cached:
                    logger.info(f"Cache HIT → {cache_key}")
                    return json.loads(cached) #type: ignore
            except Exception as e:
                logger.warning(f"Erro ao ler cache ({cache_key}): {e}")

            result = await func(*args, **kwargs)

            try:
                redis.setex(cache_key, ttl, _serialize(result))
                logger.info(f"Cache SET → {cache_key} | TTL: {ttl}s")
            except Exception as e:
                logger.warning(f"Erro ao salvar cache ({cache_key}): {e}")

            return result
        return wrapper
    return decorator

def redis_invalidate(*patterns: str):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            redis = RedisConfig.get_instance()

            for pattern in patterns:
                try:
                    # scan_iter busca as chaves que batem com o padrão
                    keys = list(redis.scan_iter(match=pattern))
                    if keys:
                        redis.delete(*keys)
                        logger.info(f"Cache INVALIDADO → {len(keys)} chave(s) com padrão '{pattern}'")
                    else:
                        logger.info(f"Nenhuma chave encontrada para o padrão '{pattern}'")
                except Exception as e:
                    logger.warning(f"Erro ao invalidar cache (padrão: {pattern}): {e}")

            return result
        return wrapper
    return decorator