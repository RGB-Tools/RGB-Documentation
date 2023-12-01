# System libraries

RGB system libraries represent non-applied level of RGB technology.

## Overview

All RGB system libraries can be classified into the following categories:

1. Consensus libraries
2. Standard library
3. Node-related libraries
4. Schema-specific libraries
5. Toolchain

The dependencies between these groups are strongly abstracted into four layers, such that underlying group doesn’t know anything about the libraries from the layer above.

Node-related and schema-scpecific libraries reside on the same level and must not depend on each other.

### Consensus libraries

These libraries are a part of RGB ossified client-side-validation consensus and must not be modified except of bugfixing. Usually, consensus-level libraries are named with “Core“ or “Foundation” as a part of their name.

1. Client-side-validation foudation library&#x20;
2. Bitcoin common libraries: implementation of parsing bitcoin data related to bitcoin consensus layer. Currently, there are split in two groups:
   1. Rust bitcoin ecosystem, maintained by Rust bitcoin community (mostly Blockstream members and Andrew Poelstra)
   2. BP Foundation Libraries, maintained by LNP/BP Standards Association, Bitcoin Protocol Working Group. Contain re-implmenetaiton or improvements of the rust-bitcoin libraries
3. Bitcoin client-side-validation, also called “BP Core Lib”. It provides primitives such as deterministic bitcoin commitments (“TapRet”, ”OpRet”) and single-use-seals.

### Standard library

Standard library (called RGB Std Lib) provides high-level convenience API for working with RGB data, but does not performes any consensus-level tasks. Any validation and RGB operations must perform without standard library, which enables use of RGB smart contract on embedded devices.

## Consensus security & maintanence

### Organizations

| GitHub Org      | Controlled by            | Main maintainers |
| --------------- | ------------------------ | ---------------- |
| bitcoin-core    | Bitcoin Core             | Peter Wuille     |
| rust-bitcoin    | Blockstream              | Andrew Poelstra  |
| rust-amplify    | Pandora Prime            | Maxim Orlovsky   |
| Strict-Encoding | LNP/BP Association \[^1] | Maxim Orlovsky   |
| AluVM           | LNP/BP Association \[^1] | Maxim Orlovsky   |
| LNP-BP          | LNP/BP Association       | Maxim Orlovsky   |
| BP-WG           | LNP/BP Association       | Maxim Orlovsky   |
| RGB-WG          | LNP/BP Association       | Maxim Orlovsky   |

\[^1]: It can be that these GitHub ogranisations will be moved to a different non-profit or a for-profit controlling body outside of the scope of LNP/BP Standards Association.

### Crates

<table><thead><tr><th width="207">Repo (crate)</th><th width="187">GitHub Org</th><th width="138">Maintained by</th><th>Description</th></tr></thead><tbody><tr><td>rust-secp256k1 (secp256k1)</td><td>bitcoin-core</td><td>Bitcoin Core</td><td></td></tr><tr><td>rust-lnpbp (lnpbp_secp256k1)</td><td>LNP-BP</td><td>LNP/BP Association</td><td>Fork of Grin re-implementation of rust-secp256k1-zkp; used for bulletproofs only</td></tr><tr><td>bitcoin_hashes</td><td>rust-bitcoin</td><td>Blockstream</td><td></td></tr><tr><td>rust-bitcoin (bitcoin)</td><td>rust-bitcoin</td><td>Blockstream</td><td></td></tr><tr><td>rust-amplify (amplify)</td><td>rust-amplify</td><td>Pandora Prime</td><td></td></tr><tr><td>rust-stens (stens)</td><td>Strict-Encoding</td><td>LNP/BP Association  [^1]</td><td>Data encoding used in RGB</td></tr><tr><td>rust-aluvm (aluvm)</td><td>AluVM</td><td>LNP/BP Association  [^1]</td><td>Virtual machine used in RGB</td></tr><tr><td>client_side_validation</td><td>LNP-BP</td><td>LNP/BP Association</td><td>Abstract client-side-validation</td></tr><tr><td>bp-foundation</td><td>BP-WG</td><td>LNP/BP Association</td><td>Bitcoin primitives (alternative to rust-bitcoin)</td></tr><tr><td>bp-core</td><td>BP-WG</td><td>LNP/BP Association</td><td>Client-side-validation for bitcoin protocol</td></tr><tr><td>rgb-core</td><td>RGB-WG</td><td>LNP/BP Association</td><td>RGB consensus library</td></tr></tbody></table>
