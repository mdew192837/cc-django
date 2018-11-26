from requests_html import HTMLSession

BASE_URL = "http://www.uschess.org/msa/thin.php?"

ID = 14986830

session = HTMLSession()

response = session.get(BASE_URL + str(ID))

rating_input = response.html.find("input[name=rating1]", first=True)

rating_value_string = rating_input.attrs["value"]

rating_value = int(rating_value_string[:rating_value_string.find("*")])

print(rating_value)