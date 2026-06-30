from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/customers", methods=["GET"])
def get_customers():
    return jsonify({
        "customers": [
            {"id": 1, "name": "John Doe", "ssn": "123-45-6789", "cc": "4111111111111111"},
            {"id": 2, "name": "Jane Smith", "ssn": "987-65-4321", "cc": "5500005555555559"}
        ]
    })

@app.route("/api/customers", methods=["POST"])
def create_customer():
    data = request.get_json()
    return jsonify({"status": "created", "received": data}), 201

@app.route("/api/customers/<int:cid>", methods=["PATCH"])
def update_customer(cid):
    data = request.get_json()
    return jsonify({"status": "updated", "id": cid, "data": data})

@app.route("/api/customers/<int:cid>", methods=["DELETE"])
def delete_customer(cid):
    data = request.get_json(silent=True)
    return jsonify({"status": "deleted", "id": cid, "data": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80 ,debug=False)
