from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/api/v1/balance', methods=['GET'])
def get_balance():
    # In a real app, this would query the isolated Database
    return jsonify({
        "union": "Nsongwa Credit Union",
        "account": "NCU-1002",
        "balance": "500,000 XAF",
        "status": "Securely Verified"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
