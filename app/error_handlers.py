from flask import jsonify

from app import app


@app.errorhandler(404)
def resource_not_found(error):
    response = jsonify(dict(
        status=404, error='Not found', message='The '
        'requested URL was not found on the server.'
    ))
    response.status_code = 404
    return response


@app.errorhandler(500)
def internal_server_error(error):
    response = jsonify(dict(
        status=500, error='Internal server error',
        message="The server "
        "encountered an internal error and was unable "
        "to complete your request."))
    response.status_code = 500
    return response
