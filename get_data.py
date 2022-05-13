from ast import parse
import traceback
import requests
import json
from moore_to_hex import mooreToHex

def getGapData(cid, pageId, depId):
    # get data from api
    api_key = "sUUYuywr9UU9HK8vYHJau88omwJoxQhs"
    api_url = f"https://api.gap.com/ux/web/productdiscovery-web-experience/products/us/gap?cid={cid}&pageId={pageId}&department={depId}"
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return data

def getOldnavyData(cid, pageId, depId):
    
    # get data from api
    api_key = "sUUYuywr9UU9HK8vYHJau88omwJoxQhs"
    
    api_url = f"https://api.gap.com/ux/web/productdiscovery-web-experience/products/us/on?cid={cid}&pageId={pageId}&department={depId}"
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return data

def getBananaData(cid, pageId, depId):
    
    # get data from api
    api_key = "sUUYuywr9UU9HK8vYHJau88omwJoxQhs"
    
    api_url = f"https://api.gap.com/ux/web/productdiscovery-web-experience/products/us/br?cid={cid}&pageId={pageId}&department={depId}"
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return data


def getAthletaData(cid):
    
    # get data from api
    api_key = "sUUYuywr9UU9HK8vYHJau88omwJoxQhs"
    
    api_url = f"https://api.gap.com/ux/web/productdiscovery-web-experience/products/us/at?cid={cid}"
    headers = {
        "Accept": "application/json",
        "apikey": api_key
    }
    response = requests.get(api_url, headers=headers)
    data = response.json()
    return data






def parseData(api_response):
    data = api_response
    # get list of products
    alldata = data["productCategoryFacetedSearch"]
    product_count = alldata["totalItemCount"]
    print(f"Total number of products: {product_count}")

    categories = alldata["productCategory"]
    this_category = categories["name"]
    print(f"Category: {this_category}")
    all_products = {}
    childCategories = categories["childCategories"]
    # return str(childCategories.keys())
    for child in childCategories:
        
        # make child into valid json
        childProducts = child["childProducts"]
        # return childProducts
        products = []
        for product in childProducts:
            try:
                product_dict = {}
                product_dict["name"] = product["name"]
                product_dict["price"] = product["price"]['currentMaxPrice']
                product_dict['quicklookImage'] = product['quicklookImage']['path']

                product_dict['productId'] = product['businessCatalogItemId']
                product_dict["inStock"] = product["isInStock"]
                product_dict["category"] = child["name"]
                product_dict["reviewScore"] = product["reviewScore"]
                product_dict["reviewCount"] = product["reviewCount"]

                products.append(product_dict)
            except TypeError as e:
                continue
        all_products[child["name"]] = products
    return all_products
        

def parseData2(api_response):
    data = api_response
    categories = data["productCategoryFacetedSearch"]["productCategory"]["childCategories"]
    # categories = categories
    # return product_list
    all_products = []
    for i in range(len(categories)):
        products = categories[i]["childProducts"]
        productList = []
        # categoryId = category["businessCatalogItemId"]

        # childProducts = category["childProducts"]
        
    

        for product in products:
   
            try:
                name = product["name"]
                oldPrice = product["price"]["localizedRegularMaxPrice"]
                price = product["price"]["currentMaxPrice"]
                isClearanceItem = product["price"]["isClearanceItem"]
                isInStock = product["isInStock"]
                mainImage = product["categoryLargeImage"]["path"]
                productId = product["businessCatalogItemId"]
                baseColorId = product["displayColor"]["baseColorId"]
                # colorCode = mooreToHex(baseColorId)
                product_dict = {
                    "name": name,
                    "oldPrice": oldPrice,
                    "price": price,

                    "isClearanceItem": isClearanceItem,
                    "isInStock": isInStock,
                    "mainImage": mainImage,
                    "productId": productId,
                    "colorCode": mooreToHex(baseColorId)

                }
            
            
            except Exception as e:
                all_products.append(product_dict)
            

            # return product_dict
            try:
                all_products.append(product_dict)
                # return productList

            except Exception as e:
                return "ERROR FUCK" + str(e)
        # return productList
        if (len(productList) > 0):
            all_products.append(productList)

    return all_products

        # all_products.append(productList)
    # return length of list
    # return all_products
    
    
    
# clear the console





def parseOldnavy(api_response):
    data = api_response
    # return data
    categories = data["productCategoryFacetedSearch"]["productCategory"]["childCategories"]
    # return categories
    # categories = categories
    # return product_list
    all_products = []
    for i in range(len(categories)):
        products = categories[i]["childProducts"]
        productList = []
        # categoryId = category["businessCatalogItemId"]

        # childProducts = category["childProducts"]
        


        for product in products:

            try:
                name = product["name"]
                oldPrice = product["price"]["localizedRegularMaxPrice"]
                price = product["price"]["currentMaxPrice"]
                isClearanceItem = product["price"]["isClearanceItem"]
                isInStock = product["isInStock"]
                mainImage = product["categoryLargeImage"]["path"]
                productId = product["businessCatalogItemId"]
                baseColorId = product["displayColor"]["baseColorId"]
                # colorCode = mooreToHex(baseColorId)
                product_dict = {
                    "name": name,
                    "oldPrice": oldPrice,
                    "price": price,

                    "isClearanceItem": isClearanceItem,
                    "isInStock": isInStock,
                    "mainImage": mainImage,
                    "productId": productId,
                    "colorCode": mooreToHex(baseColorId)

                }
            
            
            except Exception as e:
                all_products.append(product_dict)
            

            # return product_dict
            try:
                all_products.append(product_dict)
                # return productList

            except Exception as e:
                return "ERROR FUCK" + str(e)
        # return productList
        if (len(productList) > 0):
            all_products.append(productList)

    return all_products


def parseBanana(api_response):
    data = api_response

    # return data
    categories = data["productCategoryFacetedSearch"]["productCategory"]["childCategories"]
    # return categories
    # categories = categories
    # return product_list
    all_products = []
    for i in range(len(categories)):
        products = categories[i]["childProducts"]
        productList = []
        # categoryId = category["businessCatalogItemId"]

        # childProducts = category["childProducts"]
        


        for product in products:

            try:
                name = product["name"]
                oldPrice = product["price"]["localizedRegularMaxPrice"]
                price = product["price"]["currentMaxPrice"]
                isClearanceItem = product["price"]["isClearanceItem"]
                isInStock = product["isInStock"]
                mainImage = product["categoryLargeImage"]["path"]
                productId = product["businessCatalogItemId"]
                baseColorId = product["displayColor"]["baseColorId"]
                # colorCode = mooreToHex(baseColorId)
                product_dict = {
                    "name": name,
                    "oldPrice": oldPrice,
                    "price": price,

                    "isClearanceItem": isClearanceItem,
                    "isInStock": isInStock,
                    "mainImage": mainImage,
                    "productId": productId,
                    "colorCode": mooreToHex(baseColorId)

                }
            
            
            except Exception as e:
                all_products.append(product_dict)
            

            # return product_dict
            try:
                all_products.append(product_dict)
                # return productList

            except Exception as e:
                return "ERROR FUCK" + str(e)
        # return productList
        if (len(productList) > 0):
            all_products.append(productList)

    return all_products

def parseAthleta(api_response):
    data = api_response

    # return data
    categories = data["productCategoryFacetedSearch"]["productCategory"]["childCategories"]
    # return categories
    # categories = categories
    # return product_list
    all_products = []
    for i in range(len(categories)):
        products = categories[i]["childProducts"]
        productList = []
        # categoryId = category["businessCatalogItemId"]

        # childProducts = category["childProducts"]
        


        for product in products:

            try:
                name = product["name"]
                oldPrice = product["price"]["localizedRegularMaxPrice"]
                price = product["price"]["currentMaxPrice"]
                isClearanceItem = product["price"]["isClearanceItem"]
                isInStock = product["isInStock"]
                mainImage = product["categoryLargeImage"]["path"]
                productId = product["businessCatalogItemId"]
                baseColorId = product["displayColor"]["baseColorId"]
                # colorCode = mooreToHex(baseColorId)
                product_dict = {
                    "name": name,
                    "oldPrice": oldPrice,
                    "price": price,

                    "isClearanceItem": isClearanceItem,
                    "isInStock": isInStock,
                    "mainImage": mainImage,
                    "productId": productId,
                    "colorCode": mooreToHex(baseColorId)

                }
            
            
            except Exception as e:
                all_products.append(product_dict)
            

            # return product_dict
            try:
                all_products.append(product_dict)
                # return productList

            except Exception as e:
                return "ERROR FUCK" + str(e)
        # return productList
        if (len(productList) > 0):
            all_products.append(productList)

    return all_products


def main():
    cid_list = []
    for cid in cid_list:
        try: 
            data = getGapData(cid)
            all_products = parseData(data)
            print(all_products)
        except Exception as e:
            print(e)
            continue
    
        
def gap(cid, pageId, depId):
    try: 
        data = getGapData(cid, pageId, depId)
        # return data
        all_products = parseData2(data)

        return all_products


    except Exception as e:
        print(e)
        # return full traceback
        tb = traceback.format_exc()
        return str(tb)
        


def oldnavy(cid, pageId, depId):
    try: 
        data = getOldnavyData(cid, pageId, depId)
        # return data
        all_products = parseOldnavy(data)

        return all_products


    except Exception as e:
        print(e)
        # return full traceback
        tb = traceback.format_exc()
        return str(tb)
        
def banana(cid, pageId, depId):
    try: 
        data = getBananaData(cid, pageId, depId)
        # return data
        all_products = parseBanana(data)

        return all_products


    except Exception as e:
        print(e)
        # return full traceback
        tb = traceback.format_exc()
        return str(tb)



def athleta(cid):
    try: 
        data = getAthletaData(cid)
        # return data
        all_products = parseAthleta(data)

        return all_products


    except Exception as e:
        print(e)
        # return full traceback
        tb = traceback.format_exc()
        return str(tb)


