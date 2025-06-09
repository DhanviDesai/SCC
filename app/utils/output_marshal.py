def marshal_response(data=None, message="Request successful", status_code = 200):
    return {
        "success": True,
        "data": data,
        "message": message
    }, status_code

def marshal_error(message, code=400):
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }, code