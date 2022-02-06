import datetime
import ipaddress
from typing import Tuple
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def generate_tls_keys(k8s_namespace: str) -> Tuple[bytes, bytes]:
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "UK"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Greater London"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "London"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Clavis"),
        x509.NameAttribute(NameOID.COMMON_NAME, f"clavis"),
    ])
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # Expire in 10 years
        datetime.datetime.utcnow() + datetime.timedelta(days=3652)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
            x509.DNSName("localhost"),
            x509.DNSName(f"clavis.{k8s_namespace}"),
            x509.DNSName(f"clavis.{k8s_namespace}.svc"),
            x509.DNSName(f"clavis.{k8s_namespace}.svc.cluster.local")
        ]),
        critical=False,
    ).sign(key, hashes.SHA256())

    cert_pem = cert.public_bytes(serialization.Encoding.PEM)

    return key_pem, cert_pem
