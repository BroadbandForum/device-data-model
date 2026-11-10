# Device Certificates {.appendix .same-file}
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

Because the bundle itself is encrypted, its contents are protected across the entire delivery path. Only a trusted environment on the device, such as a Trusted Execution Environment (TEE) or other secure element can decrypt it. This secure environment can then safely import the private key into its protected storage. The associated public certificate can then be added to the device's certificate store.

This method ensures that the sensitive private key is never exposed in an unencrypted state on the operator's network or within the device's main operating system.

## Certificate Signing Requests (CSRs)

A Certificate Signing Request (CSR) is an encoded request sent from the device to a Certificate Authority (CA) to obtain a digital identity certificate. It serves as a standard method for a device to prove its identity and ownership of a public key without ever exposing the corresponding secret private key. The CSR bundles the public key with specific device details, which the CA validates before signing the request. This process generates a new certificate, ensuring the device is securely authenticated on the network without ever exposing the corresponding private key; the sensitive private keys remain safe on the local hardware.

### What is a CSR?

A CSR is a block of text containing the information required by a Certificate Authority (CA) to verify an identity and issue a digital certificate. This information includes:

*   **The Public Key**: The public portion of a key pair generated by the device.
*   **The Distinguished Name (DN)**: Information identifying the device, such as its Common Name (e.g., a domain name or serial number), organization, and location.
*   **The Signature**: The CSR is signed using the corresponding private key, which proves that the applicant possesses the private key.

### Procedure

![CSR Provisioning](/images/csr_provisioning_detailed.png)

The process of obtaining a certificate using a CSR typically follows these steps:

#. The device connects to the remote management server using its standard embedded key pair.
#. The management server requests the device to generate a new CSR.
#. The device creates a new key pair within its secure storage.
#. The device creates a CSR that includes its public key and identifying information.
#. The device signs the CSR with its newly generated private key.
#. The device notifies and provides the remote management server with the new CSR.
#. The remote management server will ask the Certificate Authority to generate and sign the new certificate.
#. The remote management server will install the new certificate on the device.
#. The device will use the new certificate and private key for its intended purpose.

## Advanced Certificate Management

Next to installing pre-packaged certificate bundles, the device can also support a more granular set of operations for managing the lifecycle of certificates and cryptographic keys. These procedures allow for the creation of Certificate Signing Requests (CSRs), the secure addition and deletion of certificates, and the management of cryptographic keys.

### Creating a Certificate Signing Request (CSR)

The `CreateCSR()` command allows the device to generate a new key pair and a corresponding CSR.

The command takes several input parameters to specify the details of the requested certificate:

*   `KeyType`: The type of asymmetric key pair to create. This is a free-form string. Common examples include `RSA`, `ECDSA with P-256`, `ECDSA with P-384`, `Ed25519`, and `Ed448`.
*   `KeyLength`: The length of the key in bits. Valid key lengths depend on the chosen `KeyType`. For example, RSA typically uses 2048 or 4096 bits, ECDSA with P-256 uses 256 bits, and Ed25519 uses 256 bits.
*   `SubjectAlternativeName`, `CommonName`, `OrganizationName`, `OrganizationalUnit`, `Locality`, `State`, `Country`, `Email`: These parameters define the subject identity for the certificate. At least one of `SubjectAlternativeName` or `CommonName` must be specified to identify the certificate subject. The remaining Distinguished Name (DN) fields are optional. Note that which fields are required or recommended may depend on the Certificate Authority's policy.
*   `BasicConstraints` (optional): Specifies whether the certificate is for a CA (`CA`) or an end-entity (`EndEntity`). This is optional in the CSR, as the CA may apply its own policy.
*   `KeyUsage` (optional): The cryptographic operations for which the certificate public key may be used. Values include `DigitalSignature`, `KeyEncipherment`, `KeyCertSign`, `CRLSign`, etc. This is optional in the CSR, as the CA may apply its own policy.
*   `ExtendedKeyUsage` (optional): The purposes for which the certificate public key may be used. This is a list that can include values such as `ServerAuth`, `ClientAuth`, `CodeSigning`, `EmailProtection`, `TimeStamping`, `OCSPSigning`, and `Any`. This is optional in the CSR, as the CA may apply its own policy.
*   `Name`: User-defined name to identify and categorize the certificate (e.g., "mqtt-broker", "webserver", "vpn-client"). The implementation may use this name to determine which secure storage to use and how to persist the key.
*   `RenewalInterval`: The number of days before expiration to automatically create a new CSR to update the certificate.

Example of a `CreateCSR()` command:
```
Device.Security.CreateCSR(
  Name: "mqtt-broker",
  KeyType: "RSA",
  KeyLength: 2048,
  CommonName: "mydevice.bbf.org",
  OrganizationName: "BBF",
  Country: "US",
  BasicConstraints: "EndEntity",
  KeyUsage: ["DigitalSignature", "KeyEncipherment"],
  ExtendedKeyUsage: ["ServerAuth", "ClientAuth"],
  RenewalInterval: 30
)
```
Upon successful execution, the command returns a `CommandKey`, which echoes the `command_key` supplied in the USP Operate message. This value can be used to correlate the CSR creation request with the resulting CSR entry, events, and eventually the installed certificate.

#### Concurrent and Overlapping CSR Requests

Several situations can result in multiple CSR operations targeting the same certificate `Name`. The following scenarios describe the expected behavior in each case.

**Controller retries `CreateCSR()`**

If a Controller calls `CreateCSR()` while a CSR with the same `Name` is already pending, the device rejects the new request with a 7005 (Resources Exceeded) fault code, following the concurrent operations rules defined in {{bibref|TR-369|Section 7.7.5}}.
To replace the pending CSR, the Controller must first cancel the in-progress operation via `Device.LocalAgent.Request.{i}.Cancel()`.
This causes the device to delete the CSR entry and, if not referenced by an existing certificate entry, its associated private key. The Controller can then call `CreateCSR()` again with the desired parameters.

**Controller calls `CreateCSR()` while auto-update is in progress**

When the device initiates a CSR automatically as part of an auto-update cycle, a pending CSR entry appears in `Device.Security.CSR.{i}.` just as it would for a manually triggered request. 
If the Controller calls `CreateCSR()` for the same `Name` while this auto-update CSR is pending, the device returns 7005 (Resources Exceeded).
The Controller can either wait for the auto-update cycle to complete or cancel the pending CSR via `Device.LocalAgent.Request.{i}.Cancel()`, which causes the device to remove the CSR entry and its associated private key (unless already referenced by an existing certificate entry), and then issue its own `CreateCSR()`.

**Auto-update triggers while a Controller's CSR is pending**

If the auto-update timer fires while a Controller-triggered CSR for the same `Name` is already pending, the device MUST NOT generate a new CSR.
Per R-OPR.3 of {{bibref|TR-369}}, an Agent must not cancel an operation already in progress unless explicitly instructed by the Controller.
The auto-update trigger is effectively deferred until the pending CSR resolves, either by a successful `AddCertificate()` or by `CSRTimeout` expiry.

**`CSRTimeout` expiry**

If no matching certificate is installed before `Device.Security.CSRTimeout` expires, the CSR entry is deleted.
Its associated private key is also deleted, unless it is already referenced by an existing certificate entry.
For example, in `Renew` mode where the existing key pair is reused.
The existing certificate remains valid and in service throughout.
For auto-update scenarios, the device re-evaluates the auto-update condition at the next check interval and generates a new CSR if the certificate is still within the `RenewalInterval` window.

### Adding a New Certificate

Once a CSR has been signed by a CA and a new certificate is issued, the `AddCertificate()` command is used to install it on the device.

This command takes the following parameters:

*   `Certificate`: The new certificate in PEM format. The device parses the certificate to extract and populate the Certificate table parameters including BasicConstraints, KeyUsage, and ExtendedKeyUsage extensions.
*   `Name` (optional): User-defined name to identify the certificate. When `MatchToCSR` is `true`, the name from the matching CSR is used instead. When `MatchToCSR` is `false`, this parameter MUST be specified. If a certificate with the same name already exists, it will be replaced.
*   `MatchToCSR`: A boolean that, when `true`, indicates that the new certificate is in response to a previously generated CSR. This allows the device to associate the new certificate with the correct private key and name from the matching CSR. The matching CSR is then deleted.
*   `RenewalMode` (mandatory): The automatic certificate update mode (`None`, `Renew`, or `ReKey`) to apply to the installed certificate.
*   `RenewalInterval` (mandatory): Number of days before expiry at which the device automatically initiates a new CSR, as determined by `RenewalMode`. A value of 0 disables auto-update.

If a certificate with the same `Name` already exists, the existing certificate entry is replaced with the new certificate. This replacement involves:

#. The old certificate and its associated private key are securely deleted
#. The new certificate is added with the new private key (from the matching CSR)
#. The `Name` is assigned to the new certificate entry

If the operation fails, the device returns a fault code indicating the specific error condition:

*   If `MatchToCSR` is `true` and no matching CSR was found, the device returns a 7268 (No Matching CSR) fault code.
*   If the certificate could not be imported, the device returns a 7263 (Failed To Import Certificate) fault code.
*   If the certificate has a SerialNumber and Issuer that match an existing certificate with a different `Name`, the device returns a 7270 (Certificate Identity Conflict) fault code. This prevents inconsistencies where the same certificate (identified by SerialNumber and Issuer) would be associated with multiple different names.

### Deleting a Certificate

Certificates can be deleted directly via the object-level `Delete()` command on the specific certificate entry.

Example of deleting a certificate:
```
Device.Security.Certificate.10.Delete()
```

When a certificate is deleted, its associated private key is also securely removed from the device's secure storage.

The device SHOULD immediately prevent the deleted certificate from being used to establish new connections or sessions. Active connections that were established using the deleted certificate MAY be terminated immediately or allowed to complete naturally, depending on the implementation.

The Controller SHOULD ensure a replacement certificate is available before deleting a certificate that is actively in use by a critical service. In particular, deleting the certificate used to authenticate the USP management connection may result in loss of connectivity to the Controller.

## Installing Certificate Bundles

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

The `Name` parameter allows the controller to assign a name to the certificate. If a certificate with the same `Name` already exists, it will be replaced with the certificate from the bundle.

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

If the operation fails, the device returns a fault code indicating the specific error condition (e.g., 7260 for unsupported bundle format, 7261 for signature verification failure, 7270 if the certificate in the bundle has a SerialNumber and Issuer matching an existing certificate with a different Name).

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

## Security Fault Codes

The following table lists all fault codes used by the security-related commands:

| Fault Code | Description | Used By Command(s) |
|------------|-------------|-------------------|
| **7260** | Bundle Format Not Supported | AddCertificateBundle() |
| **7261** | Bundle Signature Failure | AddCertificateBundle() |
| **7262** | Failed To Import Bundle | AddCertificateBundle(), AddCABundle(), CABundle.{i}.Update() |
| **7263** | Failed To Import Certificate | AddCertificateBundle(), AddCABundle(), CABundle.{i}.Update(), AddCertificate() |
| **7264** | Failed To Import Private Key | AddCertificateBundle() |
| **7265** | Invalid PEM Format | AddCABundle(), CABundle.{i}.Update() |
| **7266** | Insufficient Disk Space | AddCABundle(), CABundle.{i}.Update() |
| **7267** | Duplicate CA Bundle Name | AddCABundle() |
| **7268** | No Matching CSR | AddCertificate() |
| **7270** | Certificate Identity Conflict | AddCertificate(), AddCertificateBundle() |
