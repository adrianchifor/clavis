# Clavis*

**[In Development]**

Lightweight, opinionated, paranoid, k8s-native secrets management.

<img src="./docs/logo.jpeg">

\* _'key' in latin_

---

## Project objectives

- Small footprint and easy to deploy/operate
- Good cryptography practices and encryption at rest + in transit
- Granular but flexible Kubernetes-aware access control, least-privilege
    - No 'read all' permission so no leaks due to misconfiguration
    - Users can only write/update and delete, k8s service accounts read specific secrets
    - Simple cli+API for managing secrets and policies
- Comprehensive auditing and telemetry
- Secrets injection at runtime, exposed only in-memory/tmpfs, no env vars
- No lock-in, portable and extensible (init with shamir split keys, auto-unseal with \<cloud provider\> KMS)
- (nice to have) Sync secrets with 1Password vaults

## Ser, but why?

1. The built-in k8s secrets model is not safe by default, and is hard to get right:
    - base64 is not encryption. Sure you can encrypt etcd, but what about RBAC? One misconfiguration and you can read all secrets. There are many layers to get right until k8s secrets are deemed safe
1. Encrypting secrets in code is fine, but:
    - Tools like [sops](https://github.com/mozilla/sops) or [kapitan](https://kapitan.dev/secrets/) are almost impossible to audit, as often the same KMS key is used for all secrets in an environment.
    - The secrets in code usually end up just creating k8s secrets, so we're back to point 1.
1. GCP/AWS secret manager is also fine, but:
    - One IAM misconfiguration and you can read all secrets
    - Not portable, locked-in to cloud provider
    - Can get expensive
1. Hashicorp Vault is excellent, but it's hard to deploy properly and operate, and has too many knobs to configure
1. [Secrets don't belong in environment variables](https://diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/)