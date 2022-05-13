from database import getAllProducts, insert_fixed_products, update_product
hex = "#008080"








def identify_color(hex_code):
    print(hex_code)
    # remove the # from the hex code
    # if has a #
    if hex_code[0] == "#":
        hex_code = hex_code.lstrip('#')


    color_options = {
    "red": "FF0000",
    "green": "00FF00",
    "blue": "0000FF",
    "yellow": "FFFF00",
    "black": "000000",
    "white": "FFFFFF",
    "purple": "800080",
    "orange": "FFA500",
    "brown": "A52A2A",
    "grey": "808080",
    "pink": "FFC0CB",
    "teal": "008080",
    "maroon": "800000",
    "lime": "00FF00",
    "tan": "D2B48C",
}

    # return the color name with a value closest to the hex code
    return min(color_options, key=lambda color: abs(int(color_options[color], 16) - int(hex_code, 16)))



# for each product, sort the hex code


# get all products
data = list(getAllProducts())
length = len(data)
progress = 0
for product in data:
    hexColorCode = product["colorCode"]
    # if hexColorCode is a hex code
    if hexColorCode[0] == "#":
        newColorCode = identify_color(hexColorCode)
        product["colorCode"] = newColorCode
        update_product(product["_id"], product)
        progress += 1
        print(f"PRODUCT {product['productId']} COMPLETED")
        percent_done = str(round(progress/length*100, 2)) + "%"
        print(percent_done)
    else:
        print(f"PRODUCT {product['productId']} FAILED")
        pass



