from typing import Any, Optional
from fastapi import status

def success_response(
    message: str = "요청이 성공적으로 처리되었습니다.",
    status_code: int = status.HTTP_200_OK,
    data: Optional[Any] = None,
) -> dict:
    """
    통일된 성공 응답을 반환합니다. FastAPI에서 자동으로 JSONResponse로 처리됩니다.
    """

    return {
        "success": True,
        "code": status_code,
        "message": message,
        "data": data if data is not None else {},
    }

