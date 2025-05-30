from rest_framework.response import Response
from rest_framework import status


def custom_error_response(message: str, status_code: int) -> Response:
    """
    This function returns a custom error response.

    Args:
        message (str): The error message.
        status_code (int): The status code.

    Returns:
        Response: The custom error response.
    """
    error_dict = {
        "status": "error",
        "status_code": status_code,
        "message": message
    }

    return Response(error_dict, status=status_code)


def custom_success_response(data: dict, status_code: int = status.HTTP_200_OK) -> Response:
    """
    This function returns a custom success response.

    Args:
        data (dict): The success data.
        status_code (int): The status code.

    Returns:
        Response: The custom success response.
    """
    success_dict = {
        "status": "success",
        "status_code": status_code,
        "data": data
    }

    return Response(success_dict, status=status_code)
