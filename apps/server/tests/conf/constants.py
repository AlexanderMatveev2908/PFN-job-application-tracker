import os


PAYLOAD_REGISTER = {
    "first_name": "John",
    "last_name": "Doe",
    "email": f"{os.urandom(16).hex()}@gmail.com",
    "password": "qcxd-0KK64BVu5Z84DY5@czE6{!^zI_a2e9^{P(#",
    "confirm_password": "qcxd-0KK64BVu5Z84DY5@czE6{!^zI_a2e9^{P(#",
    "terms": True,
}
