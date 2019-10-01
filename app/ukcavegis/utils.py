def extract_with_css(response, query):
    return_value = response.css(query).extract_first()
    if (return_value):
        return return_value.strip()
    else:
        return None

def extract_with_xpath(response, query):
    return_value = response.xpath(query).extract_first()
    if(return_value):
        return return_value.strip()
    else:
        return None
