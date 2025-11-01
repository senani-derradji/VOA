import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.utils.logging_logs import get_logger
from app.utils.random_data import generate_random_word
from app.models.secrets import SecretVersionModel

logger = get_logger(__name__)


def check_TTL(db: Session, model, option: str):
    now = datetime.utcnow()
    expired_items = db.query(model).filter(model.expired_at <= now).all()

    if not expired_items:
        logger.info(f"No expired {option}s found at {now}")
        return

    logger.info(f"Found {len(expired_items)} expired {option}(s). Starting rotation...")

    for item in expired_items:
        name = getattr(item, "name", None) or getattr(item, "username", None)
        logger.warning(f"{option.capitalize()} expired: {name}")

        version_number = len(item.versions) + 1 if hasattr(item, "versions") else 1
        old_version = SecretVersionModel(
            secret_id=item.id,
            value=item.value,
            version_number=version_number,
            created_at=datetime.utcnow()
        )
        db.add(old_version)

        new_secret = generate_random_word()

        item.value = new_secret
        item.created_at = datetime.utcnow()
        item.expired_at = datetime.utcnow() + timedelta(seconds=30)

        logger.info(f"{option.capitalize()} rotated with new secret for: {name}")

    db.commit()
    logger.info(f"Rotation process finished for {len(expired_items)} {option}(s) at {datetime.utcnow()}")
