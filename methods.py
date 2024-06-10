import requests

base_url = "SEU_IP_UNIFI_AQUI"


def login(username, password):
    login_url = f"{base_url}/api/login"
    data = {"username": username, "password": password}
    session = requests.Session()
    response = session.post(login_url, json=data, verify=False)

    if response.status_code == 200:
        return session
    else:
        return 400


def create_voucher(session, dias, quant, dispo, setor, nome):
    notas = ' - '.join([nome, setor, dispo])
    create_url = f"{base_url}/api/s/default/cmd/hotspot"
    payload = {
        "cmd": "create-voucher",
        "expire": dias * 1440,
        "n": quant,
        "note": notas
    }
    headers = {"Content-Type": "application/json"}
    response = session.post(create_url, json=payload, headers=headers, verify=False)
    if response.status_code == 200:
        created_time = response.json()
        created_time = created_time['data'][0]['create_time']
        return created_time
    else:
        return response.text


def detalhes_voucher(session, create_time):
    vouchers = []
    detalhes_url = f"{base_url}/api/s/default/stat/voucher"
    payload = {
        "create_time": create_time
    }
    response = session.get(detalhes_url, json=payload, verify=False)
    data = response.json()

    for n in data['data']:
        vouchers.append(n['code'])

    return vouchers



def revoke_voucher(session, code):
    revoke_url = f"{base_url}/api/s/default/cmd/hotspot"
    payload = {
        '_id': code,
        'cmd': 'delete-voucher'
    }
    response = session.post(revoke_url, json=payload, verify=False)
    if response.status_code == 200:
        print('Voucher excluido com exito', response.text)
    else:
        print('Algo deu errado: ', response.text)