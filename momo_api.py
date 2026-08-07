import uuid
import os
import requests
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

# Fix: pass unique name as the first argument instead of using keyword argument 'name='
momo_bp = Blueprint('momo_api_unique', __name__, url_prefix='/api/billing')

MOMO_BASE_URL = os.environ.get("MOMO_BASE_URL", "https://sandbox.momodeveloper.mtn.com")
SUBSCRIPTION_KEY = os.environ.get("MOMO_COLLECTION_PRIMARY_KEY", "")
API_USER = os.environ.get("MOMO_COLLECTION_USER_ID", "")
API_SECRET = os.environ.get("MOMO_COLLECTION_API_SECRET", "")

@momo_bp.route('/pay-as-you-go', methods=['POST'])
@jwt_required()
def trigger_pay_as_you_go():
    current_user_id = get_jwt_identity()

    data = request.get_json() or {}
    phone_number = data.get('phone_number')
    amount = data.get('amount')
    currency = data.get('currency', 'EUR')
    
    if not phone_number or not amount:
        return jsonify({"status": "error", "message": "Phone number and amount are required."}), 400

    external_id = str(uuid.uuid4())

    try:
        token_url = f"{MOMO_BASE_URL}/collection/token/"
        auth_response = requests.post(
            token_url,
            auth=(API_USER, API_SECRET),
            headers={"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY}
        )
        
        if auth_response.status_code != 200:
            return jsonify({"status": "error", "message": "Authentication failed", "details": auth_response.text}), 400

        access_token = auth_response.json().get("access_token")

        pay_url = f"{MOMO_BASE_URL}/collection/v1_0/requesttopay"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Reference-Id": external_id,
            "X-Target-Environment": os.environ.get("MOMO_ENVIRONMENT", "sandbox"),
            "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "amount": str(amount),
            "currency": currency,
            "externalId": external_id,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": "Authorize payment for Nsongwa Credit Union SaaS",
            "payeeNote": f"User ID {current_user_id} SaaS Fee"
        }

        pay_response = requests.post(pay_url, json=payload, headers=headers)

        if pay_response.status_code in [202, 201]:
            return jsonify({
                "status": "pending",
                "message": "Payment prompt sent to phone.",
                "transaction_ref": external_id,
                "user_id": current_user_id
            }), 202
        else:
            return jsonify({"status": "error", "message": pay_response.text}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
