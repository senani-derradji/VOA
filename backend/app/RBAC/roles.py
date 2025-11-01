import os,sys

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(backend_dir)

from fastapi import Depends, HTTPException, status
from app.core.deps import get_current_user
from app.utils.logging_logs import get_logger

logger = get_logger(__name__)


def admin_required(current_user=Depends(get_current_user), func=str()):
    if current_user.role != "admin":
        logger.warning(f"Access denied {func} - {current_user.username}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    else:
        logger.info(f"Access granted {func}-{current_user.username}")
        return True

def CEO_required(current_user=Depends(get_current_user), func=str()):
    if current_user.role != "CEO":
        logger.warning(f"Access denied {func} - {current_user.username}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    else:
        logger.info(f"Access granted {func}-{current_user.username}")
        return True
