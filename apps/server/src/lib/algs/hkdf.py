from cryptography.hazmat.primitives import hashes, hmac as chmac
from cryptography.hazmat.primitives.kdf.hkdf import HKDFExpand

from src.lib.data_structure import h_to_b


MASTERS: dict[int, bytes] = {
    0: h_to_b(
        "da8d5119a6850ce5415f7602e01228fefd96d74092922a21aef8da09f60412f3dfa3362f00488733aeaf6a87e15c39446ce31c06c51d74e9621be5b271e0f680ffa23200fd26e34b45ce258bb648db7aeb3f578c92b1407c3d2d755766c23fd53ec14bbd"  # noqa: E501
    )
}


def derive_hkdf(
    *, master: bytes, info: bytes, salt: bytes
) -> dict[str, bytes]:
    h = chmac.HMAC(salt, hashes.SHA256())
    h.update(master)
    prk = h.finalize()

    okm = HKDFExpand(
        algorithm=hashes.SHA256(),
        length=64,
        info=info,
    ).derive(prk)

    return {"k_0": okm[:32], "k_1": okm[32:]}
