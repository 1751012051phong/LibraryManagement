from library import app
from flask import jsonify, request, make_response
import json
from library.BLL import RevenueSvc


@app.route('/admin/revenue-management', methods=['POST', 'GET'])
def Revenue():
    revenue_count = RevenueSvc.Revenue()
    return jsonify(revenue_count)
