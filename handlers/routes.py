from functools import lru_cache
from flask import Flask, jsonify, request
import requests
import json

def configure_routes(app):
    
    @app.route("/api/ping", methods=['GET'])
    def route_one():
        return jsonify({'success':True}), 200

    @lru_cache()
    @app.route("/api/posts", methods=['GET'])
    def route_two():
        data = []
        tags_r = request.args.get("tags", None, str)
        sort = request.args.get("sortBy", "id")
        direction = request.args.get("direction", "asc")
        #Send error messages if url is missing tags
        if tags_r is None:
            return jsonify({'error': 'Missing tags parameter'}), 400
        #Send error messages if url is contains invalid sortBy parameter
        if sort not in ["likes", "reads", "popularity", "id"]:
            return jsonify({"error": "Invalid sortBy parameter"}), 400
        #Send error message if url contains invalid direction parameter
        if direction not in ["asc", "desc"]:
            return jsonify({"error": "Invalid direction parameter"}), 400
        #Parse Tags
        tags = tags_r.strip().lower().split(",")
        try:
            for tag in tags:
                params = {
                'tag': tag
                }
                r = requests.get('https://api.hatchways.io/assessment/blog/posts', params=params).json()
                data += r["posts"]
            #Sort and Direction Parameters applied 
            if direction == "desc":
                data = sorted(data, key=lambda x: x[sort], reverse=True)
            else:
                data = sorted(data, key=lambda x: x[sort], reverse=False)
        
            return {"posts": data}, 200
        #If request fails
        except:
            return jsonify({"error": "Unkown"}), 400