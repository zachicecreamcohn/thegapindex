import requests
import os
from database import getAllProducts, insert_fixed_products, update_product

def getHTML(pid, business):

    gap_url = f"https://www.gap.com/browse/product.do?pid={pid}"
    old_navy = f"https://oldnavy.gap.com/browse/product.do?pid={pid}"
    banana = f"https://bananarepublic.gap.com/browse/product.do?pid={pid}"
    athleta = f"https://www.athleta.gap.com/browse/product.do?pid={pid}"

    if business == "gap":
        url = gap_url
    elif business == "oldnavy":
        url = old_navy
    elif business == "banana":
        url = banana
    elif business == "athleta":
        url = athleta
    
    r = requests.get(url)
    return r.text



def check_data(pid):


    gap_url = f"https://www.gap.com/browse/product.do?pid={pid}"
    old_navy = f"https://oldnavy.gap.com/browse/product.do?pid={pid}"
    banana = f"https://bananarepublic.gap.com/browse/product.do?pid={pid}"
    athleta = f"https://athleta.gap.com/browse/product.do?pid={pid}"

    businesses = ["gap", "oldnavy", "banana",]
    for business in businesses:
        html = getHTML(pid, business)
        if html.find("Sorry, this page cannot be displayed.") != -1:
            print(f"{pid} is not available in {business}")
        elif html.find("We're sorry. We couldn't find any items that matched your search term.") != -1:
            print(f"{pid} is not available in {business}")
        elif html.find("This was so wanted, it sold out.") != -1:
            print(f"{pid} is not available in {business}")
        else:
            if business == "gap":
                return gap_url
            elif business == "oldnavy":
                return old_navy
            elif business == "banana":
                return banana
            else:
                return False
    return athleta

    return "shit"


data = list(getAllProducts())


#length = number of products without a url
length = 0
for product in data:
    if 'URL' not in product:
        length += 1

completed = 0
for product in data:
    # if product has key URL, it's already fixed
    if "URL" in product:
        pass
    else:
        try:
            id = product['_id']

            pid = product["productId"]
            print(f"Checking {pid}")
            # break
            # exit()
            correct_link = check_data(pid)
            if correct_link:
                product["URL"] = correct_link
                completed += 1
            else:
                product["URL"] = "N/A"
                completed += 1
            
            update_product(id, product)
            print(f"PRODUCT {pid} COMPLETED")
        except:
            print(f"PRODUCT {pid} FAILED")
            pass

        completion_status = str(round(completed/length*100, 2)) + "%"
        print(completion_status)





# insert_fixed_products(data)


# data = list(getAllProducts())

# # print the number of products in data with a URL
# url_count = 0
# for product in data:
#     # check if product has key URL
#     if "URL" in product:
#         if product["URL"] != "N/A":
#             url_count += 1

# print(url_count)

        