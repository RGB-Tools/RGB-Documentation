# Invoices

This section explores **how invoices are structured and operate within a particular** [contract](glossary.md#contract). The initial focus is on RGB identifiers, which are integral to the operation of the system and may be encountered by users in various forms. These identifiers are unique to each component of the system, including contracts, assets, and interfaces, ensuring a standardized method of identification throughout the system.

## Identifiers and their Encoding

Each element within the system, be it a contract, schema, interface, interface or asset is assigned a **unique identifier.** These identifiers are not arbitrary strings but are carefully encoded using base58, a method chosen for its efficiency and readability. Furthermore, these identifiers are prefixed with a descriptor (in the form of a URL or URN) indicating their type, such as <mark style="color:red;">`rgb:`</mark> . This prefixing strategy ensures clarity regarding the nature of each identifier, preventing confusion with other URL and misuse.

## Enhancing Human Readability through Chunking

The concept of chunking have been introduced as a means to **enhance the readability and verifiability** of these identifiers. This technique, commonly used in phone and credit card numbers, breaks down long strings into smaller, more manageable segments. This feature not only aids in human parsing but also in verification processes, where checking the integrity of an identifier involves examining specific segments, such as the checksum at the end. Chunking, thereby, offers a balance between security and usability, with each chunk providing a certain level of security assurance. For example, having 256-bit strings divided into six blocks means that each chunk adds about 256/6 (\~42) bits of security.

An identifier for an RGB contract could be represented, by the following <mark style="color:orange;">`ContractId`</mark> encoded string:&#x20;

<mark style="color:orange;">`2WBcas9-yjzEvGufY-9GEgnyMj7-beMNMWA8r-sPHtV1nPU-TMsGMQX`</mark>

which, as we said, is a string in _Base58_ divided into the various chunks to make it easier to read. The last group of characters is a _checksum_ of the previous encoding. Finally, Base58 encoding was choose in favor of [Bech32](https://en.bitcoin.it/wiki/Bech32) encoding which can have some limitations regarding readability and character size limits of the string.

## Use of URLs for Invoices

A significant advantage of this identifier system is its compatibility with URLs, allowing for direct interaction with wallets through simple clicks. This contrasts sharply with the cumbersome process required by other systems, where multiple steps are needed to copy and paste identifiers into wallets.&#x20;

An example of a  Invoice URL for fungible tokens might be:&#x20;

<mark style="color:red;">`rgb`</mark>`:`<mark style="color:orange;">`2WBcas9-yjzEvGufY-9GEgnyMj7-beMNMWA8r-sPHtV1nPU-TMsGMQX`</mark>`/`<mark style="color:blue;">`RGB20`</mark>`/`<mark style="color:purple;">`100`</mark>`+utxob:`<mark style="color:green;">`egXsFnw-5Eud7WKYn-7DVQvcPbc-rR69YmgmG-veacwmUFo-uMFKFb`</mark>

Where

* &#x20;<mark style="color:red;">**`rgb:`**</mark> defines the application identifier of the URL.
* The <mark style="color:orange;">`ContractId`</mark> is the same as in the previous example.&#x20;
* <mark style="color:blue;">`RGB20`</mark> defines the default [interface](glossary.md#interface) which should be used to parse the contract.&#x20;
* The number <mark style="color:purple;">`100`</mark> is part of the assignment and represents the amount of  requested tokens by invoice's issuer. &#x20;
* The string  <mark style="color:green;">`egXsFnw-...`</mark>  which follows   `+utxob`  identifier is itself in the Base58 format divided into chunks, but it is neither a Bitcoin address nor a `OpId`. Indeed it is the [concealed form](../rgb-state-and-operations/components-of-a-contract-operation.md#seal-definition) of the [seal definition](glossary.md#seal-definition) that prevents Alice from knowing the UTXO actually held by Bob.

The URL format's simplicity and efficiency in opening wallets and facilitating transactions underscore its superiority over alternatives. Alternatives to the direct use of contract IDs, for example by using asset tickers, were considered but ultimately rejected due to security concerns and the potential for confusion. The chosen format prioritizes clarity and security, ensuring that users can easily understand and verify the details of their transactions.

The power of URLs is also expressed in the ease with which parameters such as an **invoice signature** can be introduced:&#x20;

<mark style="color:red;">`rgb:`</mark><mark style="color:orange;">`2WBcas9-yjzEvGufY-9GEgnyMj7-beMNMWA8r-sPHtV1nPU-TMsGMQX`</mark>`/`<mark style="color:blue;">`RGB20`</mark>`/`<mark style="color:purple;">`100`</mark>`+utxob:`<mark style="color:green;">`egXsFnw-5Eud7WKYn-7DVQvcPbc-rR69YmgmG-veacwmUFo-uMFKFb`</mark><mark style="color:yellow;">`?sig`</mark><mark style="color:yellow;">`=6kzbKKffP6xftkxn9UP8gWqiC41W16wYKE5CYaVhmEve`</mark>

With this invoice URL format each software is to be able to interpret the part of the invoice which it is able to execute while the other parts (e.g. the <mark style="color:yellow;">`?sig`</mark> part relate signature verification) can be safely discarded.

As for an extra example, in the box below an example of NFT transfer invoice is shown:&#x20;

<mark style="color:red;">`rgb:`</mark><mark style="color:orange;">`7BKsac8-beMNMWA8r--3GEprtFh7-bjzEvGufY-aNLuU4nSN-MRsLOIK`</mark>`/`<mark style="color:blue;">`RGB21`</mark>`/`<mark style="color:purple;">`DbwzvSu-4BZU81jEp-E9FVZ3xj-cyuTKWWy-2gmdnaxt-ACrS`</mark>`+utxob:`<mark style="color:green;">`egXsFnw-5Eud7WKYn-7DVQvcPbc-rR69YmgmG-veacwmUFo-uMFKFb`</mark>&#x20;

Where, in addition to the already described fields, the <mark style="color:purple;">`DbwzvSu-...`</mark> field refers to the possibility to explicitly refer to the blob of the NFT data by the receiver.

## Use of URL for Operations

As an additional example, RGB URLs can be used also for more complex operations, for instance those related to the encoding of an **issuance operation** of an RGB20-interfaced contract which assigns an amount of 10000 new tokens to the issuer wallet:

&#x20;<mark style="color:red;">`rgb:`</mark><mark style="color:orange;">`2WBcas9-yjzEvGufY-9GEgnyMj7-beMNMWA8r-sPHtV1nPU-TMsGMQX/`</mark><mark style="color:blue;">`RGB20`</mark>`/issue/`<mark style="color:purple;">`100000`</mark>`+utxob:`<mark style="color:green;">`egXsFnw-5Eud7WKYn-7DVQvcPbc-rR69YmgmG-veacwmUFo-uMFKFb`</mark>

***
