from maxma import Maxma
import json

def log(data):

    print()
    print(json.dumps(data, sort_keys=True, ensure_ascii=False, indent=4))
    print()


maxma = Maxma("f7594ef8-3cac-4d99-9f87-a2f047a4ef04")

phoneNumber = "+79218017021"
card = "34229637350689"
email = "sergh@gmail.com"
orderId = "ORDER-02437"

order_guid="729dc81b-456c-482b-9cfc-7979fd665c44"
fullName = "Sergey Safonov" 
birthdate = "1967-11-21T00:00:00+04:00"
gender = 1
amountDelta = 100
code = "5432"
shop_code = "your-shop.com"
shop_name = "YourShop.com"
qtu = 1
sku = "BN3994-049"
blackPrice = 1000
txid = "tx-011"


log(
    maxma.set_order(shop_code, orderId, phoneNumber, shop_name, blackPrice, sku, qtu)
)

