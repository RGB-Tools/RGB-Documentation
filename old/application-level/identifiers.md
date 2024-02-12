# Identifiers

RGB contracts, assets, interfaces, schemata, transfers and many other entities are identified by a specially-designed id system based on Baid58 encoding, which is Base58 enhanced with optional hardened checksum, human-readable type information and mnemonic.

All ids RGB works with are either representable as

* URLs, for ids which may be supported by client-facing software (wallets etc),
* URNs, for other ids which don't have a specific location and can't be "opened" by software,

## URL ids

### Contract ID

The main URL-based id is the RGB contract id, which can be extended into an asset id and invoice (these three are just different ways of structuring an URL):

`rgb:2dKWFWQ-agjeDw9c-3JK88KD2-5rvYcg5P-BBBaCtPX-z2us1q3n-YVVKRf`

The contract id contains 49 or 50 unique characters, including an embedded checksum (last 6 characters). To check that two IDs are equal, it is required to check at least the correspondence of the checksum (last 6 or 7 chars) + any other segment of 8 (initial) or 9 (following segments) characters, which provides \~84 bits of security.

### Secret seals

Secret seals are provided as a part of an invoice and are encoded with `utxob` URL scheme prefix, optionally using chunked string. Id always contains an embedded checksum and doesn't use a mnemonic representation.

`utxob:2eFrirU-RjqLnqR74-AKRfdnc9M-DpvSRjmZG-mFPrw7nvu-Te1wy83`

Wallets may register to handle `utxob` URL scheme and use this identifier to open a specific invoice or payment from the past.

### Transfer Consignment ID

When parties send a transfer to each other they have an option to notify about the transfer status. Thus, each transfer has its own unique id, which is the hash computed from the transfer consignment. This ID is structured like an URL, in order to allow users to launch a wallet application - with the wallet trying to locate/download consignment using URL components

`consign:2dKWFWQ-agjeDw9c-3JK88KD2-5rvYcg5P-BBBaCtPX-z2us1q3n-YVVKRf?endpoints=<list-of-endpoints>#three-mnemonic-words`

### Contract-attached File ID

RGB contracts may contain BLOBs/file objects as a part of their state. These objects are transferred as a part of the consignment, thus are always present in the local RGB stash (thus, the URL scheme is called `stashfs`). RGB wallets may register themselves to open these files. The URL has the form of

`stashfs:2dKWFWQ-agjeDw9c-3JK88KD2-5rvYcg5P-BBBaCtPX-z2us1q3n-YVVKRf#three-mnemonic-words`

## URN ids

All URN-based IDs used by the system are not intended to be "openable" by software. They are all optionally equipped with dashed three-word lowercase mnemonic following the main id after `#`. The mnemonic is given as a simple way for the user to check for typos or miscopied and is not intended as hacker protection.

<table><thead><tr><th width="241">ID class</th><th>Prefix</th></tr></thead><tbody><tr><td>Interface</td><td><code>urn:lnp-bp:if:</code></td></tr><tr><td>Schema (smart contract)</td><td><code>urn:lnp-bp:sc:</code></td></tr><tr><td>Interface implementation</td><td><code>urn:lnp-bp:im:</code></td></tr><tr><td>Semantic type</td><td><code>urn:ubideco:semid:</code></td></tr><tr><td>Strict type library</td><td><code>urn:ubideco:stl:</code></td></tr><tr><td>Strict type system</td><td><code>urn:ubideco:sts:</code></td></tr><tr><td>AluVM libary</td><td><code>urn:ubideco:alu:</code></td></tr></tbody></table>

