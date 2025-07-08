from typing import Any, Optional
from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    message: str = "요청이 성공적으로 처리되었습니다.",
    status_code: int = status.HTTP_200_OK,
    data: Optional[Any] = None,
) -> JSONResponse:
    """
    통일된 성공 응답을 반환합니다.

    :param message: 응답 메시지
    :param status_code: HTTP 상태 코드
    :param data: 응답 데이터
    :return: JSON 형식의 응답
    """

    response_body = {
        "success": True,
        "code": status_code,
        "message": message,
        "data": data if data is not None else {},
    }

    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(response_body)
    )
