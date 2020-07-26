import os
import time
from jwcrypto import jwk, jwt
import uuid
import requests
import json
import urllib
from urllib.parse import urlparse
import re
from datetime import datetime, timedelta
import webbrowser


# The software statement ID (software_id) of the software statement created in software statements (MIT).
SOFTWARE_STATEMENT_ID = ">> SOFTWARE STATEMENT ID <<"

#  Value of the kid parameter associated with the signing certificate generated in Generate a
# transport/signing certificate pair (please note that you need to use the signing certificate kid).
KID = ">> KID <<"
# Your private signing key. You will use this to sign your JWT.
PRIVATE_RSA_KEY = """
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAzzTvJs1eDlBr7DdjpJNSKBqmFmWad4HQT4D5Q0wLWw6yCGDM
S0JH9UYyY1BlDFxkyfn+jmbV5HZVIzNMLz6L0kC/yAGHGIy8Ejb1Te5zVPGv7Uio
KvEQH5dZZ9JeWKzehD5s8MXY1NRMdsQD8F1/sa4pUfgodEcTDfZIjcRyHi19aYNB
AGS/k0YR4Id9zBqpl4eXKqi5YCbCoSUBBRb7gPgCn/ZNKIgpv7KkhWTX6YO4lT9k
zjjyKBnHY/boUWu5ddKSUjWiXPKRyXz9JbRM48/85LQCp5sLl6d2QfyIOcXA8I3t
CV76gqC1vLkW4dhQA2QNz/8TNZFpBrT2dtY/KQIDAQABAoIBADbaF3kZIo39giRd
IVae3T/alh8VtIdwaPmy9cl35wWq5TxMi6hcmnn2pD4gOS/FgbTqJhYCaRr6rF0O
JlvXXeJB28MRjHbWQq87t0JzHjrdZCoXctUzTYZfZX6TdQBaeuldMS+n4Feu/7Ls
/vHxfm1F4pBddjAZ5JRsnxZQa7lK7Y/Ke+1wGbJXTTXG+T0nb00wrzvMpRFbJ5WC
JiJlXdTul+B7nA/M783AAz18Ns86FmO9HSqW6Wh7JAmcPqac5wzwyW4QAze1pdJZ
5frltjW16PnDJJdwjc5fnmbgKUiAPbZlcCWgLtLWplGKo/oId8hzJqEph5XQ+f3m
2gV5PYECgYEA69TESZVB3cwWZ/saa/Yv2skt0l9W0sxl1ZLI0Lm3kCtoSLVpxtbP
N25gcwQ5za4OAjbHxm4PaIDe5qjr2fmh9FtkJ60z+ziEtkcxv8QsL8sRAyf5Qud5
dQ2Om4EuHDvd6jIdn573zGF9gB1WGcGZiT7Zou3uvDaD38YqBxdektECgYEA4O14
9DPvHcTemfVrMgf1kqqkQA7M6GRiSFdNbFuNdE0ot9lo/8xnKRTW4OaIzy/7MymE
A9du2J75LU15/Kre1OEuS/gid0N2d5E7It4eyNWTTX8bbKbHR0HRAulRVXMl8Xjg
jqaHSEqUcaHK4JuNvOl5xY2sKnFycJUB/JqqDNkCgYAT09Gk9h2RjkUb/OqdxRcE
6AEoPMfJ9VFigXLMybB7OIsOAeKgyxKk8Gy/fs11U3ruCLkHH92/xYX4Ep+xteE9
8CkdhNxn9LqDsLyoCNBGPGZzw3qbe2akxr0Eqfm8efQQaqI+91iSIGgyy0Sf6b0E
4vndTu/RdyvjNn/2FKro4QKBgCQys3uBfCLrUvOuBmFX3JKM+cABYcKonRSNUD13
Am3MGRh1WauJBrUa0HYDQ9MsIp4aOU+w9PrRosJCrLYX/aJ+1seNGGbfKYqWidDT
tFqX3IvlP9GdiYaTNgLk75zz2hBhZqoubKkar4cWBaNeBVJ4tIsxgJqYBVXO9THk
5icJAoGBAJ/RNLNDG7pneb0MsgBFezZSZ0v07iweM+EdwS3+qA5h/zTzHPyzPl1E
SCgszWAQXW3WhXKfM+TngBSneeERwYdoSxMLRkEQTy9+2mhmLVo6ULn23835Y1rQ
9lOVWCPTE7/PwBfPr3KCrdxux3mW3iWJ4C7fvjFF8NmNdEr74aIK
-----END RSA PRIVATE KEY-----
"""

OIDC_CLIENT_ID="805de1d1-fdc8-4e02-89ac-ff2f1487112f"
OIDC_SECRET="bb5b2072-6885-4d19-b8c3-f734e65b11c6"

#  Path to transport certificate and key
# TRANSPORT_CERT_KEY = "C:\\Users\\familia\\Desktop\\amigu\\TPP225\\Banco_1/certs/client_private_key.key"
# TRANSPORT_CERT = "C:\\Users\\familia\\Desktop\\amigu\\TPP225\\Banco_1\\certs\\client_certificate"
TRANSPORT_CERT_KEY = "C:/Users/familia/Desktop/amigu/TPP225/Banco_1/certs/client_private_key.key"
TRANSPORT_CERT = "C:/Users/familia/Desktop/amigu/TPP225/Banco_1/certs/client_certificate"

V3_ACCT_BASEURL = "https://rs1.o3bank.co.uk/open-banking/v3.1/aisp/"
V3_PYMT_BASEURL = "https://rs1.o3bank.co.uk/open-banking/v3.1/pisp/"

def make_token(kid: str, model_bank_client_id: str) -> str:
    jwt_iat = int(time.time())
    jwt_exp = jwt_iat + 600
    header = dict(alg='PS256', kid=kid, typ='JWT')
    claims = dict(
        iss=model_bank_client_id,
        sub=model_bank_client_id,
        aud="https://as1.tecban-sandbox.o3bank.co.uk/token",
        jti=str(uuid.uuid4()),
        iat=jwt_iat,
        exp=jwt_exp
    )
 
    token = jwt.JWT(header=header, claims=claims)
    key_obj = jwk.JWK.from_pem(PRIVATE_RSA_KEY.encode('latin-1'))
    token.make_signed_token(key_obj)
    signed_token = token.serialize()
    return signed_token

def get_access_token(signed_token: str, model_bank_client_id: str) -> str:
    data_dict = dict(
        client_assertion_type='urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        grant_type='client_credentials',
        client_id=model_bank_client_id,
        client_assertion=signed_token,
        scope="openid accounts payments"
    )
    print(data_dict)
    client = (TRANSPORT_CERT, TRANSPORT_CERT_KEY)
    response = requests.post(
        'https://as1.tecban-sandbox.o3bank.co.uk/token',
        data=data_dict,
        verify=False,
        cert=client
    )
    print(response)
    print(response.json().get('access_token'))
    return response.json().get('access_token')
    
get_access_token(make_token(KID, OIDC_CLIENT_ID), OIDC_CLIENT_ID)