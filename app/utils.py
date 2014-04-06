from flask import make_response

def cors_response(response):
    resp = make_response(response)
    resp.headers['Access-Control-Allow-Origin'] = "http://localhost:4567"
    return resp
