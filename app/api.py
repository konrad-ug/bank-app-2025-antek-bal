from flask import Flask, request, jsonify
from src.account_registry import AccountRegistry
from src.personal_account import PersonalAccount
from src.company_account import CompanyAccount

app = Flask(__name__)
account_registry = AccountRegistry()

@app.route("/api/personal_accounts", methods=['POST'])
def create_personal_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = PersonalAccount(data.get("first_name"), data.get("last_name"), data.get("pesel"), data.get("promo_code"))
    account_registry.add_personal_account(account)
    return jsonify({"message": "Account created"}), 201


@app.route("/api/personal_accounts", methods=['GET'])
def get_all_personal_accounts():
    print("Get all accounts request received")
    accounts = account_registry.return_personal_accounts()
    accounts_data = [
        {"first_name": acc.first_name, "last_name": acc.last_name, "pesel": acc.pesel, "balance": acc.balance} for acc
        in accounts]
    return jsonify(accounts_data), 200


@app.route("/api/personal_accounts/count", methods=['GET'])
def get_personal_account_count():
    print("Get account count request received")
    count = len(account_registry.personal_accounts)
    return jsonify({"count": count}), 200


@app.route("/api/personal_accounts/<pesel>", methods=['GET'])
def get_account_by_pesel(pesel):
    account = account_registry.search_personal_account(pesel)
    if account:
        return jsonify({"first_name": account.first_name, "last_name": account.last_name, "pesel": account.pesel,
                        "balance": account.balance}), 200
    return jsonify({"error": "Account not found"}), 404


@app.route("/api/personal_accounts/<pesel>", methods=['PATCH'])
def update_personal_account(pesel):
    data = request.get_json()
    account = account_registry.search_personal_account(pesel)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    if "first_name" in data:
        account.first_name = data.get("first_name")

    if "last_name" in data:
        account.last_name = data.get("last_name")

    return jsonify({"message": "Account updated"}), 200


@app.route("/api/personal_accounts/<pesel>", methods=['DELETE'])
def delete_personal_account(pesel):
    account = account_registry.search_personal_account(pesel)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    account_registry.personal_accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/personal_accounts/<pesel>/transfer", methods=['POST'])
def transfer_personal_account(pesel):
    data = request.get_json()
    account = account_registry.search_personal_account(pesel)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    transfer_type = data.get("type")
    amount = data.get("amount")

    if transfer_type == "incoming":
        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 422
        account.balance += amount
        return jsonify({"message": "Transfer in progress"}), 200

    elif transfer_type == "outgoing":
        receiver = find_receiver(data)
        if not receiver:
            return jsonify({"error": "Receiver account not found"}), 404  # lub 422

        success = account.outgoing_transfer(receiver, amount)
        if success:
            return jsonify({"message": "Transfer in progress"}), 200
        else:
            return jsonify({"error": "Insufficient funds"}), 422

    elif transfer_type == "express":
        receiver = find_receiver(data)
        if not receiver:
            return jsonify({"error": "Receiver account not found"}), 404

        success = account.express_transfer(receiver, amount)
        if success:
            return jsonify({"message": "Transfer in progress"}), 200
        else:
            return jsonify({"error": "Insufficient funds"}), 422

    else:
        return jsonify({"error": "Unknown transfer type"}), 400

@app.route("/api/personal_accounts/<pesel>/submit_for_loan", methods=['POST'])
def personal_account_submit_for_loan(pesel):
    submitter = account_registry.search_personal_account(pesel)
    data = request.get_json()
    amount = data.get("amount")

    if not submitter:
        return jsonify({"error": "Account not found"}), 404

    success = submitter.submit_for_loan(amount)
    if success:
        return jsonify({"message": "Submission for loan successful"}), 200
    return jsonify({"error": "Submission for loan failed"}), 400


@app.route("/api/personal_accounts/<pesel>/history", methods=['GET'])
def get_personal_history(pesel):
    account = account_registry.search_personal_account(pesel)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    serialized_history = []
    for data in account.history:
        data_copy = data.copy()

        identity = data.get("identity")

        if hasattr(identity, "pesel"):
            data_copy["identity"] = identity.pesel
        elif hasattr(identity, "nip"):
            data_copy["identity"] = identity.nip
        else:
            data_copy["identity"] = str(identity)

        serialized_history.append(data_copy)

    return jsonify(serialized_history), 200

@app.route("/api/company_accounts", methods=['POST'])
def create_company_account():
    data = request.get_json()
    print(f"Create account request: {data}")
    account = CompanyAccount(data.get("company_name"), data.get("nip"))
    account_registry.add_company_account(account)
    return jsonify({"message": "Account created"}), 201


@app.route("/api/company_accounts", methods=['GET'])
def get_all_company_accounts():
    print("Get all accounts request received")
    accounts = account_registry.return_company_accounts()
    accounts_data = [{"company_name": c.company_name, "nip": c.nip} for c in accounts]
    return jsonify(accounts_data), 200


@app.route("/api/company_accounts/count", methods=['GET'])
def get_company_accounts_count():
    print("Get account count request received")
    count = len(account_registry.company_accounts)
    return jsonify({"count": count}), 200


@app.route("/api/company_accounts/<nip>", methods=['GET'])
def get_account_by_nip(nip):
    account = account_registry.search_company_account(nip)
    if account:
        return jsonify({"company_name": account.company_name, "nip": account.nip, "balance": account.balance}), 200
    return jsonify({"error": "Account not found"}), 404


@app.route("/api/company_accounts/<nip>", methods=['PATCH'])
def update_company_account(nip):
    data = request.get_json()
    account = account_registry.search_company_account(nip)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    if "company_name" in data:
        account.company_name = data.get("company_name")

    return jsonify({"message": "Account updated"}), 200


@app.route("/api/company_accounts/<nip>", methods=['DELETE'])
def delete_company_account(nip):
    account = account_registry.search_company_account(nip)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    account_registry.company_accounts.remove(account)
    return jsonify({"message": "Account deleted"}), 200


@app.route("/api/company_accounts/<nip>/transfer", methods=['POST'])
def transfer_company_account(nip):
    data = request.get_json()
    account = account_registry.search_company_account(nip)

    if not account:
        return jsonify({"error": "Account not found"}), 404

    transfer_type = data.get("type")
    amount = data.get("amount")

    if transfer_type == "incoming":
        if amount <= 0:
            return jsonify({"error": "Invalid amount"}), 422
        account.balance += amount
        return jsonify({"message": "Transfer in progress"}), 200

    elif transfer_type == "outgoing":
        receiver = find_receiver(data)
        if not receiver:
            return jsonify({"error": "Receiver account not found"}), 404

        success = account.outgoing_transfer(receiver, amount)
        if success:
            return jsonify({"message": "Transfer in progress"}), 200
        else:
            return jsonify({"error": "Insufficient funds"}), 422

    elif transfer_type == "express":
        receiver = find_receiver(data)
        if not receiver:
            return jsonify({"error": "Receiver account not found"}), 404

        success = account.express_transfer(receiver, amount)
        if success:
            return jsonify({"message": "Transfer in progress"}), 200
        else:
            return jsonify({"error": "Insufficient funds"}), 422

    else:
        return jsonify({"error": "Unknown transfer type"}), 400


@app.route("/api/company_accounts/<nip>/submit_for_loan", methods=['POST'])
def company_account_submit_for_loan(nip):
    submiter = account_registry.search_company_account(nip)
    data = request.get_json()
    amount = data.get("amount")

    if not submiter:
        return jsonify({"error": "Account not found"}), 404

    success = submiter.submit_for_loan(amount)
    if success:
        return jsonify({"message": "Submission for loan successful"}), 200
    return jsonify({"error": "Submission for loan failed"}), 400


@app.route("/api/company_accounts/<nip>/history", methods=['GET'])
def get_company_history(nip):
    account = account_registry.search_company_account(nip)
    if not account:
        return jsonify({"error": "Account not found"}), 404

    history = []
    for data in account.history:
        data_copy = data.copy()

        identity = data.get("identity")

        if hasattr(identity, "pesel"):
            data_copy["identity"] = identity.pesel
        elif hasattr(identity, "nip"):
            data_copy["identity"] = identity.nip
        else:
            data_copy["identity"] = str(identity)

        history.append(data_copy)

    return jsonify(history), 200

def find_receiver(data):
    receiver_pesel = data.get("receiver_pesel")
    if receiver_pesel:
        return account_registry.search_personal_account(receiver_pesel)

    receiver_nip = data.get("receiver_nip")
    if receiver_nip:
        return account_registry.search_company_account(receiver_nip)

    return None