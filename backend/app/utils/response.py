from fastapi.responses import JSONResponse


def success(message, data=None):

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )


def error(message):

    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": message
        }
    )