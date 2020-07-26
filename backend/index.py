# import requests

# url = "https://as1.tecban-sandbox.o3bank.co.uk/token"

# payload = 'grant_type=client_credentials&scope=accounts%20openid'
# headers = {
#   'Content-Type': 'application/x-www-form-urlencoded',
#   'Authorization': 'Basic ODA1ZGUxZDEtZmRjOC00ZTAyLTg5YWMtZmYyZjE0ODcxMTJmOmJiNWIyMDcyLTY4ODUtNGQxOS1iOGMzLWY3MzRlNjViMTFjNg=='
# }

# response = requests.request("POST", url, headers=headers, data = payload)

# print(response.text.encode('utf8'))

# # Exception has occurred: SSLError
# # HTTPSConnectionPool(host='as1.tecban-sandbox.o3bank.co.uk', port=443): Max retries exceeded with url: /token (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1108)')))
# #   File "C:\Users\familia\Desktop\amigu\index.py", line 11, in <module>
# #     response = requests.request("POST", url, headers=headers, data = payload)