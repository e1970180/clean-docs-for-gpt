---
title: "Securing"
description: "Instructions on how to secure your Home Assistant installation."

related:
  - docs: /docs/configuration/
  - docs: /docs/configuration/secrets/
    title: Secrets.yaml file
  - docs: /cloud/
    title: Home Assistant Cloud
  - url: https://nabucasa.com/config/
    title: Nabu Casa
---

One major advantage of Home Assistant is that it is not dependent on cloud services. Even if you are only using Home Assistant on a local network, you should take steps to secure your instance.

## Checklist

Here's the summary of what you *must* do to secure your Home Assistant system:

- Centralize sensitive data in secrets (but do remember to back them up).
  - **Note**: Storing secrets in `secrets.yaml` does not encrypt them.
- Regularly keep the system up to date.

## Remote access

If you want secure remote access, the easiest option is to use Home Assistant Cloud by which you also support the founders of Home Assistant.

Another option is to use TLS/SSL via the add-on Duck DNS integrating Let's Encrypt.

To expose your instance to the internet, use a VPN, or an SSH tunnel. Make sure to expose the used port in your router.

### Extras for manual installations

Besides the above, we advise that you consider the following to improve security:

- For systems that use SSH, set `PermitRootLogin no` in your sshd configuration (usually `/etc/ssh/sshd_config`) and use SSH keys for authentication instead of passwords. This is particularly important if you enable remote access to your SSH services.
- Lock down the host following good practice guidance, for example:
  - Securing Debian Manual (this also applies to Raspberry Pi OS)
  - Red Hat Enterprise Linux 7 Security Guide, CIS Red Hat Enterprise Linux 7 Benchmark
