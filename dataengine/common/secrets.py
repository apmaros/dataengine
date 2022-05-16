import os
import typing as t

from dataengine.common.log import logger

SECRETS_PATH = f'/run/secrets/'


def get_secret(name: str) -> t.Optional[str]:
    """
    Retrieves a secret in following order:
        - environment variable
        - file

    Secrets in environment variable are always in uppercase and file in lowercase.
    @name: name of the secret
    :return: value of the secret
    """
    logger.debug(f"Trying to fetch secret '{name}' from environment variable")
    env_variable_secret = os.getenv(name.upper())

    if env_variable_secret is not None:
        logger.debug(f"Secret '{name}' found - using secret from environment variable")
        return env_variable_secret

    secret_path = f"{SECRETS_PATH}/{name.lower()}"
    logger.debug(f"Trying to fetch secret '{name}' from file")
    if os.path.exists(secret_path):
        logger.debug(f"Secret '{name}' found - using secret from file")
        secret = open(secret_path).read().rstrip('\n')
        return secret

    logger.error(f"Secret '{name}' was not found")
    return None
