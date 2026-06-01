# MQTT Theory of Operation {.appendix .same-file}

This section explains the operation of MQTT within the Device:2 data model. The data model manages MQTT clients and a local MQTT broker on the device, supporting TLS-encrypted connections and access control.

![MQTT Introduction Overview](/images/mqtt_introduction_overview.png)

The data model contains three main components:

*   **`Device.MQTT.Client.{i}`:** Configures an MQTT client to connect to an MQTT broker.
*   **`Device.MQTT.Broker.{i}`:** Configures a local MQTT broker listener on the device for local messaging and bridging to other brokers. Multiple listeners can share a broker process using the `BrokerID` parameter.
*   **`Device.MQTT.BrokerSecurity`:** Manages security for local MQTT broker processes, including client identities and Access Control Lists (ACLs).

## Definitions

*   **MQTT Client:** Any device or application that runs an MQTT library and connects to an MQTT broker. Clients publish messages to topics and subscribe to topics to receive messages. The `Device.MQTT.Client.{i}` object represents an MQTT client.
*   **MQTT Broker:** A server that receives messages from publishing clients, filters them, and sends them to subscribed clients. It functions as a central hub for MQTT communication. The `Device.MQTT.Broker.{i}` object represents a local broker running on the device.
*   **MQTT Bridge:** A connection that allows two or more MQTT brokers to share messages. A bridge forwards messages from topics on one broker to another. The `Device.MQTT.Broker.{i}.Bridge.{i}` object manages the bridge configuration.

## Securing Connections with TLS
An MQTT client, broker, or bridge secures its connection using Transport Layer Security (TLS) when it is configured for a secure transport (`TLS` or `WebSocketTLS`). The data model supports standard TLS (client verifies the server via certificate) and Mutual Authentication (mTLS), where both client and server verify each other's identity via certificates.

The following parameters configure these secure connections:

*   **`Username` and `Password`**: Used for basic authentication with the broker. This mechanism works for both secure TLS and non-TLS connections. The broker verifies these credentials to control access.

*   **`ClientID`**: A unique identifier used to distinguish each client connected to the broker. The broker can use the `ClientID` to enforce ACLs and manage sessions for both authenticated and anonymous clients.

*   **`Anonymous Connections`**: A client can connect anonymously if the broker permits it.

*   **`Certificate`:** A reference to an entry in the `Device.Security.Certificate.{i}` table. It specifies the certificate the entity (client or server) presents to the remote party. The server provides a certificate to the client, and the client provides a certificate only if mutual authentication is required.

*   **`CABundle`:** A reference to an entry in the `Device.Security.CABundle.{i}` table. It specifies the set of Certificate Authority (CA) certificates the entity uses to validate the certificate presented by the remote party. For mutual authentication to succeed, the client uses its `CABundle` to validate the server's `Certificate`, and the server uses its `CABundle` to validate the client's `Certificate`.

*   **`CipherList`:** A comma-separated list of cipher suites that the TLS client or server is allowed to use. This restricts the connection to strong, modern ciphers and avoids known weak algorithms.

## MQTT Client Operation

The `Device.MQTT.Client.{i}` object configures an MQTT client. Each instance of this object represents a single client and corresponds to a separate connection. A client uses TLS to establish a secure connection to an MQTT broker, configured with the parameters from the ["Securing Connections with TLS" section](#securing-connections-with-tls).

**Example of TCP/IP with anonymous authentication:**

This example shows an MQTT client (`Device.MQTT.Client.1`) that connects to a remote broker using an unencrypted TCP connection, and authenticates anonymously.

*   `Device.MQTT.Client.1.TransportProtocol` = `TCP/IP`
*   `Device.MQTT.Client.1.Username` = `""`
*   `Device.MQTT.Client.1.Password` = `""`

The client establishes a TCP connection, which is a non-encrypted connection, for anonymous authentication by the broker.

**Example of TCP/IP with username and password authentication:**

This example shows an MQTT client (`Device.MQTT.Client.2`) that connects to a remote broker using an unencrypted TCP connection, and authenticates with a username and password.

*   `Device.MQTT.Client.2.TransportProtocol` = `TCP/IP`
*   `Device.MQTT.Client.2.Username` = `myUser`
*   `Device.MQTT.Client.2.Password` = `myPassword`

The client establishes a TCP connection and sends its username and password over this non-encrypted connection for authentication by the broker.

**Example of normal TLS (client authenticates server):**

This example shows an MQTT client (`Device.MQTT.Client.3`) that connects securely to a remote broker where only the client verifies the broker's identity.

*   `Device.MQTT.Client.3.TransportProtocol` = `TLS`
*   `Device.MQTT.Client.3.Username`     = `myUser`
*   `Device.MQTT.Client.3.Password`     = `myPassword`
*   `Device.MQTT.Client.3.Certificate`  = `""`
*   `Device.MQTT.Client.3.CABundle`     = `Device.Security.CABundle.1` (The CA bundle to validate the broker's certificate)
*   `Device.MQTT.Client.3.CipherList`   = `TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384`

![MQTT Client Normal TLS](/images/mqtt_client_tls_sequence.png)

The client establishes an encrypted TLS connection, authenticating with its username and password sent over this secure channel. Since the client does not present its own certificate for authentication, the `Certificate` parameter remains empty or unset. Instead, the client focuses on validating the broker's certificate against the provided `CABundle` and negotiating one of the two specified cipher suites.

**Example of an anonymous connection over TLS:**

This example shows an MQTT client (`Device.MQTT.Client.4`) that connects securely to a remote broker where only the client verifies the broker's identity.

*   `Device.MQTT.Client.4.TransportProtocol` = `TLS`
*   `Device.MQTT.Client.4.Username`     = `""`
*   `Device.MQTT.Client.4.Password`     = `""`
*   `Device.MQTT.Client.4.Certificate`  = `""`
*   `Device.MQTT.Client.4.CABundle`     = `Device.Security.CABundle.1` (The CA bundle to validate the broker's certificate)
*   `Device.MQTT.Client.4.CipherList`   = `TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384`


The client does not present its own certificate for authentication, so the `Certificate` parameter is empty or not set. The client validates the broker's certificate against the provided `CABundle` and only negotiates one of the two specified cipher suites.

**Example of mutual authentication (mTLS):**

This example shows an MQTT client (`Device.MQTT.Client.5`) that connects securely to a remote broker using mTLS, where both the client and broker authenticate each other.

*   `Device.MQTT.Client.5.TransportProtocol` = `TLS`
*   `Device.MQTT.Client.5.Certificate` = `Device.Security.Certificate.2` (The client's own certificate to present to the broker)
*   `Device.MQTT.Client.5.CABundle` = `Device.Security.CABundle.1` (The CA bundle to validate the broker's certificate)
*   `Device.MQTT.Client.5.CipherList` = `TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384`

The client initiates a TLS connection, presents its client certificate (`Device.Security.Certificate.2`), validates the broker's certificate against `CABundle.1`, and negotiates a specified cipher suite. The broker must also be configured to request and validate the client's certificate.

![MQTT Client Mutual Authentication TLS](/images/mqtt_client_mtls_sequence.png)

## MQTT broker operation

The `Device.MQTT.Broker.{i}` object configures a local MQTT broker on the device. This broker serves two main purposes:

*   It provides a local messaging bus for applications on the device.
*   It acts as a gateway to a larger MQTT network by bridging to other brokers.

### Authentication

The `AuthenticationMethod` parameter configures how the local broker authenticates clients:

*   **`UsernamePassword`:** Clients authenticate using a username and password.
*   **`CertViaCN`:** Clients authenticate with a client certificate after a successful mTLS handshake. The Common Name (CN) from the certificate's subject serves as the username for access control.
*   **`CertViaSubject`:** Clients authenticate with a client certificate after a successful mTLS handshake. The entire certificate subject serves as the username for access control. For example, a certificate subject of `C=US, O=Example Inc, CN=device1` becomes the username for ACL matching.

If `AllowAnonymous` is `true`, clients can connect without credentials.

![MQTT Broker Authentication Flow](/images/mqtt_broker_authentication_flow.png)

**Example of broker authentication (username and password with anonymous):**

A local broker (`Device.MQTT.Broker.1`) allows both username/password authentication and anonymous access:

*   `Device.MQTT.Broker.1.AuthenticationMethod` = `UsernamePassword`
*   `Device.MQTT.Broker.1.AllowAnonymous` = `true`

Clients can connect with a valid username and password (checked against `Device.MQTT.BrokerSecurity.Client.{i}` entries) or connect anonymously. ACL rules can still apply to anonymous clients.

### Access Control

The `Device.MQTT.BrokerSecurity.ACL.{i}` table manages access control for the local broker. Each entry is an ACL rule specifying:

*   **`AllowAnonymous`:** If `true`, this rule allows access to anonymous clients.
*   **`ClientList`:** A list of clients the rule applies to, identified by their entries in the `Device.MQTT.BrokerSecurity.Client.{i}` table.
    *   **Empty `ClientList` Behavior:** An empty list means the rule can apply to any authenticated client that has an entry in `Device.MQTT.BrokerSecurity.Client.{i}`. If `AllowAnonymous` is `true`, this rule applies to all clients, including anonymous clients.
*   **`Topics`:** The MQTT topics the rule applies to.
*   **`Operations`:** The MQTT operations (`Publish` or `Subscribe`) the rule controls.
*   **`Access`:** Whether to `Allow` or `Deny` the operation.

The broker evaluates rules based on the `Order` parameter.

#### ACL evaluation logic

The broker follows an ordered evaluation to determine if an operation is permitted.

1.  **Rule Order:** Rules are processed sequentially from the lowest `Order` number to the highest.
2.  **First Match Wins:** The first rule that matches the client, topic, and operation determines the outcome. All subsequent rules are ignored.
3.  **Allow or Deny:** If the first matching rule's `Access` is `Allow`, the operation is permitted. If it is `Deny`, the operation is forbidden.
4.  **Default Deny Practice:** For security, it is good practice to end the ACL set with a final, high-order "deny-all" rule (e.g., `Order` = `999`, `Topics` = `#`, `Access` = `Deny`). This ensures any operation not explicitly allowed by a preceding rule is denied by default.

![MQTT ACL Evaluation Logic](/images/mqtt_acl_evaluation_logic.png)

### MQTT Listeners

An MQTT listener defines how the local broker accepts incoming client connections. Each `Device.MQTT.Broker.{i}` instance represents a single listener that specifies a specific endpoint where clients can connect to.

![MQTT Broker Listeners](/images/mqtt_broker_listeners.png)

Multiple listeners can be configured on different ports or with different protocols. For example, you could configure one listener on port `8883` for highly secure, certificate-based connections from trusted devices, and a second listener on port `1883` that uses a simpler username/password scheme for application access.

The broker's listener parameters are:

*   **`Port`:** The TCP port number where the broker listens for incoming connections.
*   **`Interface`:** The IP network interface the broker binds to. If left empty, it will listen on all available interfaces.
*   **`TransportProtocol`:** The protocol for the connection (e.g., `TCP/IP`, `TLS`, `WebSocket`). If you choose `TLS` or `WebSocketTLS`, the listener enforces a secure connection using the TLS parameters configured on the broker instance, such as `Certificate` and `CABundle`.

### Broker Process Management

The `BrokerID` parameter controls how listener instances are grouped into broker processes:

*   Same BrokerID: Multiple `Device.MQTT.Broker.{i}` instances with the same `BrokerID` value run in the same broker process.
*   Different BrokerID: Instances with different `BrokerID` values run as separate broker processes, providing isolation between different broker processes.

### End-to-End Broker Configuration Example

This example demonstrates how to configure a local MQTT broker to manage various client types and security requirements. It sets up the broker to:

*   Listen for secure mTLS connections on port `8883`, specifically for trusted devices like sensors and administrators.
*   Listen for username/password and anonymous connections on port `1883`, accommodating standard users and guest clients.
*   Authenticate clients based on their certificate's Common Name (CN) for mTLS connections, or a traditional username/password for other connections.
*   Control client access to topics using a detailed set of Access Control List (ACL) rules, ensuring each client type has appropriate permissions.
*   Handle various client interactions, such as:
    *   A secure sensor (`my-sensor-1`) publishing data to its designated topic.
    *   An administrator (`admin`) subscribing to all sensor data.
    *   A standard user (`user1`) publishing and subscribing within their personal topic space.
    *   An anonymous client publishing telemetry data to a specific topic.
    *   Rejecting connections from clients with invalid certificates or unauthorized access attempts.

**1. Broker Listener and Authentication Configuration:**

The first step configures the broker's listeners and their authentication methods. Setting up two listeners on two different broker instances shares the same security configuration.

**Listener 1: mTLS on Port 8883**

*   `Device.MQTT.Broker.1.Enable` = `true`
*   `Device.MQTT.Broker.1.Port` = `8883`
*   `Device.MQTT.Broker.1.TransportProtocol` = `TLS`
*   `Device.MQTT.Broker.1.AuthenticationMethod` = `CertViaCN`
*   `Device.MQTT.Broker.1.AllowAnonymous` = `false`
*   `Device.MQTT.Broker.1.Certificate` = `Device.Security.Certificate.3` (The broker's server certificate)
*   `Device.MQTT.Broker.1.CABundle` = `Device.Security.CABundle.2` (The CA bundle to validate client certificates)

This configuration makes the broker listen on port 8883 for mTLS connections, expect client certificates, and use the certificate's Common Name for authentication.

**Listener 2: Username/Password and Anonymous on Port 1883**

*   `Device.MQTT.Broker.2.Enable` = `true`
*   `Device.MQTT.Broker.2.Port` = `1883`
*   `Device.MQTT.Broker.2.TransportProtocol` = `TCP/IP`
*   `Device.MQTT.Broker.2.AuthenticationMethod` = `UsernamePassword`
*   `Device.MQTT.Broker.2.AllowAnonymous` = `true`

This sets up a second listener on port 1883 for standard TCP/IP connections, allowing both username/password authentication and anonymous access.

**2. Client Identity Definitions:**

Next, define the client identities the broker will recognize. The `Username` must match either the CN from the client's certificate for mTLS or the provided username for password authentication.

*   **Client Identity for Sensor 1 (mTLS):**
    *   `Device.MQTT.BrokerSecurity.Client.1.Name` = `SensorClient1`
    *   `Device.MQTT.BrokerSecurity.Client.1.Username` = `my-sensor-1` (Expected CN)
    *   `Device.MQTT.BrokerSecurity.Client.1.Enable` = `true`

*   **Client Identity for Admin User (mTLS):**
    *   `Device.MQTT.BrokerSecurity.Client.2.Name` = `AdminUser`
    *   `Device.MQTT.BrokerSecurity.Client.2.Username` = `admin` (Expected CN)
    *   `Device.MQTT.BrokerSecurity.Client.2.Enable` = `true`

*   **Client Identity for User 1 (Username/Password):**
    *   `Device.MQTT.BrokerSecurity.Client.3.Name` = `User1`
    *   `Device.MQTT.BrokerSecurity.Client.3.Username` = `user1`
    *   `Device.MQTT.BrokerSecurity.Client.3.Password` = `secret`
    *   `Device.MQTT.BrokerSecurity.Client.3.Enable` = `true`

**3. Access Control List (ACL) Rules:**

Finally, configure the ACL rules for the defined identities. The rules are evaluated by `Order`, from lowest to highest.

*   **Rule A (Order 10): Allow `SensorClient1` to publish to its own topic.**
    *   `Device.MQTT.BrokerSecurity.ACL.1.Order` = `10`
    *   `Device.MQTT.BrokerSecurity.ACL.1.ClientList` = `Device.MQTT.BrokerSecurity.Client.1`
    *   `Device.MQTT.BrokerSecurity.ACL.1.Topics` = `sensors/temp/my-sensor-1`
    *   `Device.MQTT.BrokerSecurity.ACL.1.Operations` = `Publish`
    *   `Device.MQTT.BrokerSecurity.ACL.1.Access` = `Allow`

*   **Rule B (Order 20): Allow `AdminUser` to subscribe to all sensor data.**
    *   `Device.MQTT.BrokerSecurity.ACL.2.Order` = `20`
    *   `Device.MQTT.BrokerSecurity.ACL.2.ClientList` = `Device.MQTT.BrokerSecurity.Client.2`
    *   `Device.MQTT.BrokerSecurity.ACL.2.Topics` = `sensors/#`
    *   `Device.MQTT.BrokerSecurity.ACL.2.Operations` = `Subscribe`
    *   `Device.MQTT.BrokerSecurity.ACL.2.Access` = `Allow`

*   **Rule C (Order 30): Allow `User1` to publish and subscribe to their own topics.**
    *   `Device.MQTT.BrokerSecurity.ACL.3.Order` = `30`
    *   `Device.MQTT.BrokerSecurity.ACL.3.ClientList` = `Device.MQTT.BrokerSecurity.Client.3`
    *   `Device.MQTT.BrokerSecurity.ACL.3.Topics` = `users/user1/#`
    *   `Device.MQTT.BrokerSecurity.ACL.3.Operations` = `Publish,Subscribe`
    *   `Device.MQTT.BrokerSecurity.ACL.3.Access` = `Allow`

*   **Rule D (Order 40): Allow anonymous clients to publish telemetry.**
    *   `Device.MQTT.BrokerSecurity.ACL.4.Order` = `40`
    *   `Device.MQTT.BrokerSecurity.ACL.4.AllowAnonymous` = `true`
    *   `Device.MQTT.BrokerSecurity.ACL.4.ClientList` = `"[]"` (Empty list with `AllowAnonymous`=`true` applies to all clients)
    *   `Device.MQTT.BrokerSecurity.ACL.4.Topics` = `anonymous/telemetry/#`
    *   `Device.MQTT.BrokerSecurity.ACL.4.Operations` = `Publish`
    *   `Device.MQTT.BrokerSecurity.ACL.4.Access` = `Allow`

*   **Rule E (Order 66): Deny all other operations by default.**
    *   `Device.MQTT.BrokerSecurity.ACL.5.Order` = `66`
    *   `Device.MQTT.BrokerSecurity.ACL.5.AllowAnonymous` = `true`
    *   `Device.MQTT.BrokerSecurity.ACL.5.ClientList` = `"[]"` (Empty list with `AllowAnonymous`=`true` applies to all clients)
    *   `Device.MQTT.BrokerSecurity.ACL.5.Topics` = `#`
    *   `Device.MQTT.BrokerSecurity.ACL.5.Operations` = `Publish,Subscribe`
    *   `Device.MQTT.BrokerSecurity.ACL.5.Access` = `Deny`

## MQTT bridge operation

The `Device.MQTT.Broker.{i}.Bridge.{i}` object lets the local MQTT broker connect to other (remote) MQTT brokers. This is necessary for distributed MQTT deployments.

Each `Bridge.{i}` instance defines a connection to a remote broker. If `TransportProtocol` is `TLS` or `WebSocketTLS`, the connection is secured as described in the ["Securing Connections with TLS" section](#securing-connections-with-tls).

![MQTT Broker Bridge](/images/mqtt_secure_bridge_diagram.png)

**Example of a secure MQTT bridge:**

This bridge configuration sends messages from `Device.MQTT.Broker.1` to a remote broker at `cloud.example.com` securely using mTLS:

*   `Device.MQTT.Broker.1.Bridge.1.Enable` = `true`
*   `Device.MQTT.Broker.1.Bridge.1.Name` = `CloudBridge`
*   `Device.MQTT.Broker.1.Bridge.1.TransportProtocol` = `TLS`
*   `Device.MQTT.Broker.1.Bridge.1.Server.1.Address` = `cloud.example.com`
*   `Device.MQTT.Broker.1.Bridge.1.Server.1.Port` = `8883`
*   `Device.MQTT.Broker.1.Bridge.1.Certificate` = `Device.Security.Certificate.4` (The bridge's client certificate)
*   `Device.MQTT.Broker.1.Bridge.1.CABundle` = `Device.Security.CABundle.3` (The CA bundle to validate the remote cloud broker's certificate)
*   `Device.MQTT.Broker.1.Bridge.1.Subscription.1.Topic` = `sensors/#`
*   `Device.MQTT.Broker.1.Bridge.1.Subscription.1.Direction` = `out`

This bridge establishes a secure mTLS connection to `cloud.example.com:8883`, authenticates itself with `Certificate.4`, verifies the cloud broker with `CABundle.3`, and forwards all messages from topics matching `sensors/#` to the remote broker.
