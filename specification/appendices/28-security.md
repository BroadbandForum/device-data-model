# Device Certificates
## Introduction

A device requires a secure storage mechanism for storing cryptographic assets such as certificates and private keys.

This secure storage is provisioned during manufacturing. The device certificate and its associated private key are used to establish a secure management channel, for example via CWMP or USP.

To ensure that the device connects only to an authentic management server, the firmware embeds one or more trusted Certificate Authority (CA) certificates. These CA certificates are used to validate the server’s identity during connection establishment. Mutual authentication is achieved when the server, in turn, validates the device’s certificate, resulting in a secure, bidirectionally authenticated communication channel.

A device may employ multiple certificates and private keys for different services. These credentials can be provisioned at manufacturing time as part of the firmware image, or they may be securely managed, rotated, and updated remotely by the management server throughout the device’s operational lifecycle. E.g. the management server installs a new certificate bundle on the device or the device can request a new certificate by generating a new private key and submitting a Certificate Signing Request (CSR) to a Certificate Authority.

## Secure Storage of Cryptographic Assets

The security of a device is dependent on the protection of its cryptographic assets. Private keys, in particular, must be stored in a way that prevents unauthorized access, even by privileged software running on the device's main processor or by an attacker with physical access to the hardware.

The mechanisms for storing these assets have evolved over the years to provide progressively stronger security guarantees.

### Non-Encrypted Storage

The most basic approach is to store certificates and private keys as files in a standard, non-encrypted partition of the filesystem. While simple, this method is highly insecure. An attacker who gains root access to the device or can read its flash memory directly can easily steal these sensitive credentials. Such a leak could assist in attacking the operator's servers (e.g. spoofing a trusted device) and potentially be used to gain privileged access to other devices provided by the operator.

### Encrypted Storage

A significant improvement is to store cryptographic assets within an encrypted partition. This approach ensures that a straightforward physical extraction of the flash memory does not directly expose private keys or other sensitive material.

The effectiveness of this mechanism, however, depends entirely on the protection of the partition’s decryption key. If the decryption key is stored elsewhere on the device in a reversible or recoverable form the overall security posture is compromised.

To mitigate this risk the decryption key is typically provisioned at manufacturing time and stored within the processor’s secure memory region, such as hardware-backed secure storage or one-time programmable (OTP) memory. This prevents software-level access to the key and significantly raises the bar against physical and logical attacks.

### Secure Cryptographic Storage

The industry best practice and most robust approach for protecting cryptographic assets is the use of dedicated tamper-resistant hardware. This model ensures that private keys are never exposed in plaintext outside a protected execution environment. 

Rather than extracting a key to perform a cryptographic operation the data to be processed is passed into the secure environment where the operation is executed internally. As a result, private keys are never present in nor accessible from the main operating system.

Common secure storage implementations:

* Hardware Security Module (HSM): A dedicated cryptographic processor specifically designed to protect the entire lifecycle of cryptographic keys, from generation and storage to usage and destruction.
* Soft HSM: A software-based workaround that emulates some functionalities of a Hardware Security Module. Its primary goals are to provide a consistent API (like PKCS#11) for cryptographic services and to limit the exposure of private keys in memory during runtime. This approach is often used in cost-sensitive devices that lack dedicated hardware like a TEE or SE. While it does not provide the same security guarantees as a hardware-based solution, it offers more protection than storing keys as simple plaintext files.
* Trusted Execution Environment (TEE): A secure area within the main processor that ensures code and data loaded into it are protected with respect to confidentiality and integrity.
* Trusted Element / Secure Element (SE): A tamper-resistant microcontroller capable of securely hosting applications and sensitive data, isolated from the primary system.

Access to these secure environments is typically provided through standardized APIs such as PKCS#11. These interfaces allow applications to perform cryptographic operations without requiring direct access to the underlying keys.

## Certificate Management
Digital certificates are essential for authenticating services and establishing encrypted communication, such as TLS. To prevent service disruptions from expired certificates and to mitigate risks like key compromise, certificates must be updated regularly.

A primary security requirement for these updates is that the private key must never be transmitted and stored in an unencrypted format. It must always be transported over a secure channel.

![secure-channel](/images/certificate-update.svg)

However, as [](#fig:secure-channel) illustrates, establishing a truly secure channel can be challenging. Even with TLS, aspects of the network and device architecture might still present opportunities for eavesdropping or interception.

To counter these risks, the certificate and its private key should be delivered together as an encrypted and digitally signed bundle.

A bundle is a file package (e.g., PKCS#12, PEM) that contains a service certificate and a private key. The private key within the bundle must be encrypted (e.g., password-protected).

Since the bundle itself may be unpacked in a non-secure environment on the device, it is mandatory that the private key contained within the bundle is always encrypted. This ensures that only the trusted environment with the correct decryption keys can access and use the private key, even if the bundle itself is not encrypted.

The certificate, being public information, does not require this level of protection and can be stored in the device certificate store.

Because the bundle itself is encrypted, its contents are protected across the entire delivery path. Only a trusted environment on the device, such as a Trusted Execution Environment (TEE)  or other secure element can decrypt it. This secure environment can then safely import the private key into its protected storage. The associated public certificate can then be added to the device's certificate store.

This method ensures that the sensitive private key is never exposed in an unencrypted state on the operator's network or within the device's main operating system.

## Installing Bundles

The installation process is managed by the USP Controller.

![key-store](/images/trusted-key-store.svg)

The Controller should first query which bundle formats are supported:

    Device.Security.SupportedBundleFormats
    {
        "PKCS12", "PEM"
    }

The Controller can then install a new bundle by invoking the `Device.Security.AddCertificateBundle()` USP command:

    Device.Security.AddCertificateBundle(
        Alias: 'cpe-mABR',
        Name: 'mABR',
        BundleFormat: 'PKCS12',
        Bundle: 'binary bundle payload'
    )

The device installs the new bundle and updates the `Device.Security.Certificate.{i}.` object with the new certificate's information. The command returns a path reference to the installed certificate entry.

    Device.Security.Certificate.10.
        Alias               = "cpe-mABR"
        Name                = "mABR"
        Enable              = "true"
        LastModif           = "2025-11-24T12:46:53.375021Z"
        SerialNumber        = "089233D543C0734BFF61E5680EA63E93"
        NotAfter            = "2026-09-14T23:59:59Z"
        NotBefore           = "2025-10-06T00:00:00Z"
        Subject             = "/C=US/L=ISSY LES MOULINEAUX/O=BBF/CN=mabr.preprod-tv-us-cdn.bbf.org"
        SubjectAlt          = "DNS:mabr.preprod-tv-us-cdn.bbf.org"
        SignatureAlgorithm  = "ecdsa-with-SHA384"

If the operation fails, the device returns a fault code indicating the specific error condition (e.g., 7260 for unsupported bundle format, 7261 for signature verification failure).

The URIs for the new certificate and private key can be retrieved as follows:

    Device.Security.Certificate.10.GetCertificateURI()
    {
        CertificateURI = file://foo/bar/mabr.pem
        PrivateKeyURI  = pkcs11:token=bbf;id=%01
    }

## Managing CA Certificate Bundles

The Controller can manage CA certificate bundles using the following operations:

### Adding CA Bundles

To add a new CA bundle containing one or more CA certificates:

    Device.Security.AddCABundle('TrustedRootCAs', 'PEM bundle payload')
    {
        CABundle = "Device.Security.CABundle.1."
        NumberOfCertificates = 3
    }

This creates a new entry in the `Device.Security.CABundle.{i}.` table. The command returns a path reference to the installed CA bundle entry and the number of certificates successfully installed.

If the operation fails, the device returns a fault code indicating the specific error condition (e.g., 7265 for invalid PEM format, 7267 for duplicate CA bundle name).

### Updating CA Bundles

To update an existing CA bundle with new certificates:

    Device.Security.CABundle.1.Update('new PEM bundle payload')
    {
        NumberOfCertificates = 5
    }

The update operation completely replaces the existing CA certificates. The command returns the number of certificates successfully installed. If the update fails, the previous bundle is kept as-is.

If the operation fails, the device returns a fault code indicating the specific error condition (e.g., 7265 for invalid PEM format, 7266 for insufficient disk space).
