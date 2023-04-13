import requests

from day1.constants import API_PASSWORD, API_KEY

headers = {"Accept": "application/json", "Content-Type": "application/json"}
shop_url = "https://%s:%s@deep-store-0706.myshopify.com/admin" % (API_KEY, API_PASSWORD)

def create_product():
    payload = {
        "product": {
            "title": "Product From API",
            "body_html": "Ahihi",
            "vendor": "deep-store",
            "product_type": "TestType",
            "status": "active",
            "published_scope": "global",
            "tags": [ 
                "Test",
                "Test1"
            ],
            "variants": [],
            "options": [],
            "images": [],
            "image": None,
        }
    }
    
    endpoint = "/api/2023-04/products.json"
    
    # create Product
    r = requests.post(shop_url + endpoint, json=payload, headers=headers)
    return r

def update_price(variant_id):
    
    payload = {
        "variant": {
            "price": 55000,
            "compare_at_price": 150000,
            "inventory_management": "shopify",
        }
    }
    
    endpoint = "/api/2023-04/variants/" + str(variant_id) + ".json"
    r = requests.put(shop_url + endpoint, json=payload, headers=headers)
    return r

def update_quantity(inventory_item_id, qty_available):
    tracked = {
        "inventory_item": {
            "tracked": True
        }
    }
    requests.put(shop_url + "/api/2023-04/inventory_items/" + str(inventory_item_id) + ".json", json=tracked, headers=headers)
    
    endpoint_get_level = "/api/2023-04/inventory_levels.json?inventory_item_ids=" + str(inventory_item_id)
    
    inventory_level = requests.get(shop_url + endpoint_get_level, headers=headers)
    print(inventory_level.json()["inventory_levels"][0]["location_id"])
    print(inventory_item_id)
    
    qty = {
        # "inventory_level": {
        "inventory_item_id": inventory_item_id,
        "location_id": inventory_level.json()["inventory_levels"][0]["location_id"],
        "available": qty_available,
        # }
    }
    
    endpoint_set_qty = "/api/2023-04/inventory_levels/set.json"
    
    r = requests.post(shop_url + endpoint_set_qty, json=qty, headers=headers)
    print(r.json())
    return r
    
    

def update_product(product):
    create_product_image(product.json()["product"]["id"], [])
    
    for variant in product.json()["product"]["variants"]:
        update_price(variant["id"])
        update_quantity(variant["inventory_item_id"], 10)
        
def add_option(product_id):
    payload = {
        "product": {
            "variants": [             
                {
                    "option1": "White",
                    "option2": "Medium"
                }, 
                {
                    "option1": "White",
                    "option2": "Small"
                }
            ],
            "options": [
                {
                    "position": 1,
                    "name": "Color",
                    "values": [
                        "White"
                    ]
                },
                {
                    "position": 2,
                    "name": "Size",
                    "values": [
                        "Medium",
                        "Small"
                    ]  
                },
            ],
        }
    }
    
    endpoint = "/api/2023-04/products/" + str(product_id) + ".json"
    
    r = requests.put(shop_url + endpoint, json=payload, headers=headers)
    return r


def delete_product(product_id):
    endpoint = "/api/2023-04/products/" + str(product_id) + ".json"
    
    r = requests.delete(shop_url + endpoint, headers=headers)
    
def create_custom_collection():
    
    payload = {
        "custom_collection": {
            "body_html": "<p>The best selling iPods ever</p>",
            "published_scope": "global",
            "title": "IPods",
            "collects": []
        }
    }
    
    endpoint = "/api/2023-04/custom_collections.json"
    
    r = requests.post(shop_url + endpoint, json=payload, headers=headers)
    print(r.json())
    
def create_smart_collection():
    payload = {
        "smart_collection": {
            "title": "Macbooks",
            "rules": [
                {
                    "column": "vendor",
                    "relation": "equals",
                    "condition": "Test1"
                }
            ],
        }
    }
    endpoint = "/api/2023-04/smart_collections.json"
    
    r = requests.post(shop_url + endpoint, json=payload, headers=headers)
    print(r.json())
    
def create_product_image(product_id, variant_ids):
    
    payload = {
        "image": {
            "position": 1,
            "alt": "Product Image",
            "product_id": product_id,
            "src": "https://cdn.vjshop.vn/ong-kinh/mirrorless/sigma/sigma-18-50mm-f28-dc-dn-c/for-sony-e/sigma-18-50mm-f28-dc-dn-c.jpg",
            "variant_ids": variant_ids,
        }
    }
    
    endpoint = "/api/2023-04/products/" + str(product_id) + "/images.json"
    r = requests.post(shop_url + endpoint, json=payload, headers=headers)
    
    return r

def create_customer():
    payload = {
        "customer": {
            "email": "test.lastnameson@example.com",
            "first_name": "Steve",
            "last_name": "Lastnameson",
            "currency": "VND",
            "phone": "+15142546012",
        }
    }
    
    endpoint = "/api/2023-04/customers.json"
    
    r = requests.post(shop_url + endpoint, json=payload, headers=headers)
    
    create_customer_address(r.json()["customer"]["id"])
    
    return r
    
def create_customer_address(customer_id):
    payload = {
        "customer_address": {
            "customer_id": customer_id,
            "first_name": "Samuel",
            "last_name": "de Champlain",
            "company": "Fancy Co.",
            "address1": "1 Rue des Carrieres",
            "address2": "Suite 1234",
            "city": "Montreal",
            "province": "Quebec",
            "country": "Canada",
            "zip": "G1R 4P5",
            "name": "Samuel de Champlain",
            "province_code": "QC",
            "country_code": "CA",
            "country_name": "Canada",
            "default": False
        }
    }
    
    endpoint = "/api/2023-04/customers/" + str(customer_id) + "/addresses.json"
    r = requests.post(shop_url + endpoint, json=payload, headers=headers)
    
    return r
    
def create_order(customer_email):
    payload = {
        "order": {
            "email": customer_email,
            "line_items": [
              {
                    "variant_id": 44930731344161,
                    "quantity": 2,
              },
              {
                    "variant_id": 44926353703201,
                    "quantity": 2,
              }
            ],
        }
    }
    
    endpoint = "/api/2023-04/orders.json"
    
    r = requests.post(shop_url + endpoint, json=payload, headers=headers)  
    return r  

if __name__ == '__main__':
    
    product1 = create_product()
    product1 = add_option(product1.json()["product"]["id"])
    product1 = update_product(product1)
    
    
    product2 = create_product()
    product2 = update_product(product2)
    
    # delete_product(product1.json()["product"]["id"])
    # delete_product(product2.json()["product"]["id"])

    # create_smart_collection()
    # customer = create_customer()
    # create_order("test.lastnameson@example.com")