import requests
import redis
import json

redis_db = redis.Redis(host='localhost', port=6379, db=0)


class Maxma:
    host = "https://api-test.maxma.com/"

    def __init__(self, token):
        self.req_header = {
            "X-Processing-Key": token,
        }

    def create_cliend(self, phoneNumber, email, fullName, gender, birthdate, card):
        host = self.host
        req_header = self.req_header
        payload = {
            "client": {
                "phoneNumber": phoneNumber,
                "email": email,
                "fullName": fullName,
                "gender": gender,
                "birthdate": birthdate,
                "card": card,

            }
        }
        try:
            response = requests.post(
                f"{host}new-client", headers=req_header, json=payload)

            if response.status_code == 200:
                response = response.json()
                key = "client:  " + response["client"]["phoneNumber"]
                redis_db.set(key, json.dumps(
                    response, sort_keys=True, ensure_ascii=False, indent=4))
                return response
            else:
                raise Exception("Error Code")
        except:
            print("Error")


    def find_client(self, phoneNumber):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)

            payload = {
                "phoneNumber": filt_resp['client']['phoneNumber']
            }
            response = requests.post(
                f"{host}get-balance", headers=req_header, json=payload)
            return response.json()
        except:
            print("Error")


    def update_client(self, phoneNumber, email):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)

            payload = {
                "phoneNumber": filt_resp['client']['phoneNumber'],
                "client": {
                    "email": email,
                    "isEmailSubscribed": True,
                }
            }
            response = requests.post(
                f"{host}update-client", headers=req_header, json=payload)
            if response.status_code == 200:
                response = response.json()
                key = "client:  " + response["client"]["phoneNumber"]
                redis_db.set(key, json.dumps(
                    response, sort_keys=True, ensure_ascii=False, indent=4))
                return response
            else:
                raise Exception("Error Code")
        except:
            print("Error")


    def send_conf_code(self, phoneNumber):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)

            payload = {
                "phoneNumber": filt_resp['client']['phoneNumber']
            }
            response = requests.post(
                f"{host}send-confirmation-code", headers=req_header, json=payload)
            return response.json()
        except:
            print("Error")


    def get_history(self, phoneNumber):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)

            payload = {
                "client": {
                    "phoneNumber": filt_resp['client']['phoneNumber']
                },
                "pagination": {
                    "limit": 20,
                    "offset": 0
                }
            }
            response = requests.post(
                f"{host}get-history", headers=req_header, json=payload)
            return response.json()
        except:
            print("Error")


    def adjust_balance(self, phoneNumber, amountDelta):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)

            payload = {
                "client": {
                    "phoneNumber": filt_resp['client']['phoneNumber']
                },
                "balanceAdjustment": {
                    "amountDelta": amountDelta,
                    "expirationPeriodDays": 60,
                    "notify": True,
                }
            }
            response = requests.post(
                f"{host}adjust-balance", headers=req_header, json=payload)
            if response.status_code == 200:
                response = response.json()
                key = "balance:  " + filt_resp['client']['phoneNumber']
                redis_db.set(key, json.dumps(
                    response, sort_keys=True, ensure_ascii=False, indent=4))
                return response
            else:
                raise Exception("Error Code")
        except:
            print("Error")


    def check_balance(self, phoneNumber):
        try:
            response_db = redis_db.get("balance:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)
            return filt_resp
        except:
            print("Error")


    def issue_promocode(self, phoneNumber, code):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)

            payload = {
                "client": {
                    "phoneNumber": filt_resp['client']['phoneNumber']
                },
                "code": code
            }
            response = requests.post(
                f"{host}issue-promocode", headers=req_header, json=payload)
            return response.json()
        except:
            print("Error")


    def set_purchase(self, phoneNumber, txid, shop_code, shop_name, sku, blackPrice, qtu):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)
            phoneNumber = filt_resp['client']['phoneNumber']

            payload = {
                "txid": txid,
                "calculationQuery": {
                    "client": {
                        "phoneNumber": phoneNumber
                    },
                    "shop": {
                        "code": shop_code,
                        "name": shop_name
                    },
                    "rows": [
                        {
                            "product": {
                                "sku": sku,
                                "blackPrice": blackPrice
                            },
                            "qty": qtu
                        }
                    ],
                    "applyBonuses": 200
                }
            }
            response = requests.post(
                f"{host}set-purchase", headers=req_header, json=payload)

            if response.status_code == 200:
                response = response.json()
                key = "purchase:  " + phoneNumber
                redis_db.set(key, json.dumps(
                    response, sort_keys=True, ensure_ascii=False, indent=4))
                return response
            else:
                raise Exception("Error Code")
        except:
            print("Error")


    def confirm_ticket(self, txid, phoneNumber):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)
            phoneNumber = filt_resp['client']['phoneNumber']

            order_db = redis_db.get("purchase:  " + phoneNumber).decode()
            order_db_filt = json.loads(order_db)
            ticket = order_db_filt["ticket"]

            payload = {
                "txid": txid,
                "ticket": ticket
            }
            response = requests.post(
                f"{host}confirm-ticket", headers=req_header, json=payload)

            if response.status_code == 200:
                text = "The Purchase has been Successfull !"
                response = response.json()
                redis_db.delete("purchase:  " + phoneNumber)
                return text
            else:
                raise Exception("Error Code")
        except:
            print("Error")


    def discard_ticket(self, txid, phoneNumber):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)
            phoneNumber = filt_resp['client']['phoneNumber']

            order_db = redis_db.get("purchase:  " + phoneNumber).decode()
            order_db_filt = json.loads(order_db)
            ticket = order_db_filt["ticket"]

            payload = {
                "txid": txid,
                "ticket": ticket
            }
            response = requests.post(
                f"{host}discard-ticket", headers=req_header, json=payload)

            if response.status_code == 200:
                text = "The Purchase has been canceled !"
                redis_db.delete("purchase:  " + phoneNumber)
                return text
            else:
                raise Exception("Error Code")
        except:
            print("Error")
        

    def set_order(self, shop_code, orderId, phoneNumber, shop_name, blackPrice, sku, qtu):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)
            payload = {
                "orderId": orderId,
                "calculationQuery": {
                    "client": {
                        "phoneNumber": filt_resp['client']['phoneNumber']
                    },
                    "shop": {
                        "code": shop_code,
                        "name": shop_name
                    },
                    "rows": [
                        {
                            "product": {
                                "sku": sku,
                                "blackPrice": blackPrice
                            },
                            "qty": qtu
                        }
                    ],
                    "applyBonuses": 200
                }
            }
            response = requests.post(
                f"{host}v2/set-order", headers=req_header, json=payload)
            if response.status_code == 200:
                response = response.json()
                key = "order:  " + filt_resp['client']['phoneNumber']
                redis_db.set(key, json.dumps(
                    response, sort_keys=True, ensure_ascii=False, indent=4))
                return response
            else:
                raise Exception("Error Code")
        except:
            print("Error!")


    def confirm_order(self, orderId, phoneNumber):
        host = self.host
        req_header = self.req_header
        try:
            response_db = redis_db.get("client:  " + phoneNumber).decode()
            filt_resp = json.loads(response_db)

            payload = {
                "orderId": orderId,
            }
            response = requests.post(
                f"{host}confirm-order", headers=req_header, json=payload)
            if response.status_code == 200:
                response = response.json()
                key = "confirmed-order:  " + filt_resp['client']['phoneNumber']
                redis_db.set(key, json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4))
                redis_db.delete("order:  " + filt_resp['client']['phoneNumber'])
                return response
            else:
                raise Exception("Error Code")
        except:
            print("Error")


    def cancel_order(self, orderId, phoneNumber):
        host = self.host
        req_header = self.req_header
        payload = {
            "orderId": orderId,
        }
        response = requests.post(
            f"{host}cancel-order", headers=req_header, json=payload)
        if response.status_code == 200:
            text = "The order has been canceled"
            key = "order:  " + phoneNumber
            redis_db.delete()
            return text
        else:
            raise Exception("Error Code")
