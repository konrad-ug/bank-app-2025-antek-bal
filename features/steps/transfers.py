from behave import *
import requests

URL = "http://localhost:5000"


@step('I make an incoming transfer of "{amount}" to account with pesel "{pesel}"')
def incoming_transfer(context, amount, pesel):
    json_body = {
        "type": "incoming",
        "amount": int(amount)
    }
    response = requests.post(URL + f"/api/personal_accounts/{pesel}/transfer", json=json_body)
    assert response.status_code == 200


@when('I transfer "{amount}" from account with pesel "{sender_pesel}" to account with pesel "{receiver_pesel}"')
def outgoing_transfer(context, amount, sender_pesel, receiver_pesel):
    json_body = {
        "type": "outgoing",
        "amount": int(amount),
        "receiver_pesel": receiver_pesel
    }
    response = requests.post(URL + f"/api/personal_accounts/{sender_pesel}/transfer", json=json_body)
    assert response.status_code == 200


@when('I try to transfer "{amount}" from account with pesel "{sender_pesel}" to account with pesel "{receiver_pesel}"')
def try_outgoing_transfer(context, amount, sender_pesel, receiver_pesel):
    json_body = {
        "type": "outgoing",
        "amount": int(amount),
        "receiver_pesel": receiver_pesel
    }
    context.last_response = requests.post(URL + f"/api/personal_accounts/{sender_pesel}/transfer", json=json_body)


@when(
    'I make an express transfer of "{amount}" from account with pesel "{sender_pesel}" to account with pesel "{receiver_pesel}"')
def express_transfer(context, amount, sender_pesel, receiver_pesel):
    json_body = {
        "type": "express",
        "amount": int(amount),
        "receiver_pesel": receiver_pesel
    }
    response = requests.post(URL + f"/api/personal_accounts/{sender_pesel}/transfer", json=json_body)
    assert response.status_code == 200


@then('The transfer should fail with status code {status_code}')
def check_transfer_failure(context, status_code):
    assert context.last_response.status_code == int(status_code)


@then('Account with pesel "{pesel}" has balance "{expected_balance}"')
def check_balance(context, pesel, expected_balance):
    response = requests.get(URL + f"/api/personal_accounts/{pesel}")
    assert response.status_code == 200
    account_data = response.json()
    assert float(account_data["balance"]) == float(expected_balance)
