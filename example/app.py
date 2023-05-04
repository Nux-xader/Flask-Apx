import typing as t
from flask import Flask
from hashlib import md5
from apx.auth import Auth
from apx.param import Param
from apx.helpers import ApxResp
from apx.config import ApxConfig
from flask import current_app as cr_app
from apx.route import route as apx_route
from apx.exceptions import SpecificErrResp


accounts = dict()
get_token = lambda x: md5(x.encode()).hexdigest()

app = Flask(__name__)
app.debug = True
app.secret_key = "Lorem ipsum reprehenderit commodo cupidatat officia voluptate. Culpa nulla nisi"

apx_resp = ApxResp()
apx_resp.spesific_err_msgs = (
    "wrong username or password", 
    "{} must be {}", 
    "{} must be contain minimum {} character", 
    "username not found"
)

def get_role_info(session_:str) -> t.Optional[str]:
    global accounts
    account = accounts.get(session_.get('token'))
    if account is None: return
    return account['role']

apx_auth = Auth(
    list_role=["admin", "user"], 
    get_role_info=get_role_info
)

app.apx = ApxConfig(resp=apx_resp, auth=apx_auth)


@app.route("/regist", methods=["POST"])
@apx_route()
def regist(param:Param):
    global accounts
    username:str = param.text('username', expected_type=str, is_require=True)
    password:str = param.text('password', expected_type=str, is_require=True)
    address:str = param.text('address', expected_type=str, is_require=True)
    is_admin:bool = param.text('is_admin', expected_type=bool, default_val=False)

    if not username.isalnum(): raise SpecificErrResp("1:username:alpha numeric")
    if len(password) < 8: raise SpecificErrResp("2:password:8")
    if len(address) < 5: raise SpecificErrResp("1:address:5")

    accounts[get_token(username+password)] = {
        "role": "admin" if is_admin else "user", 
        "username": username, 
        "address": address
    }

    return {"success": True}


@app.route("/login", methods=["POST"])
@apx_route()
def login(param:Param):
    global accounts
    username:str = param.text('username', is_require=True)
    password:str = param.text('password', is_require=True)

    token = get_token(username+password)
    role = get_role_info({'token': token})
    if role is None: raise SpecificErrResp("0")

    cr_app.apx.auth.update({'token': token})
    return {"success": True, "role": role}


@app.route("/account-info", methods=["GET"])
@apx_route(param=False, allowed_role=("admin", "user"))
def accoount_info():
    global accounts
    return accounts.get(cr_app.apx.auth.get().get('token'))


@app.route("/account-list", methods=["GET"])
@apx_route(param=False, allowed_role=("admin", ))
def accoount_list():
    global accounts
    return list(accounts.values())


@app.route("/delete-account", methods=["POST"])
@apx_route(allowed_role=("admin", ))
def delete_account(param:Param):
    global accounts
    username = param.text('username', expected_type=str, is_require=True)

    token = list(filter(
        lambda x: x[1] == username, 
        map(lambda x: [x[0], x[1]['username']], accounts.items())
    ))
    if len(token) == 0: raise SpecificErrResp("3")
    del accounts[token[0]]

    return {"success": True}

@app.route("/update-account", methods=["POST"])
@apx_route(allowed_role=("admin", "user"))
def update_account(param:Param):
    global accounts
    address = param.text('address', expected_type=str, is_require=True)

    if len(address) < 5: raise SpecificErrResp("1:address:5")
    accounts[cr_app.apx.auth.get().get('token')] = address

    return {"success": True}

if __name__ == "__main__":
    app.run()
