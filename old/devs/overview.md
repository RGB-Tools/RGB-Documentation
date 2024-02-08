# Overview

RGB is a complex system composed of multiple layers and multiple protocols on each of the levels. It is based on bitcoin and lightning network technologies, enhanced with client-side-validation (LNP/BP) - and adds a lot of stuff on top of them.

To reduce the level of complexity and mitigate the risks of cross-dependencies RGB developers took a layered approach, building the technology in modular way, where the modules are abstracted into a different strata - such that the strata below do not know anything about the strata above.

Overall, the development around RGB can be classified into the following fields, layered on top of each other:

* **Core protocol**, or **consensus-level development**. You may think of it as of something which means for RGB the same thing as "Bitcoin Core" means for Bitcoin.
* **Toolchain development**, which includes compilers, linkers, programming languagues and other tools. You may think of it as of Consensys company in Ethereum ecosystem.
* Schemata development
* Smart contracts issuance
* Wallet, exchange and other software integration

<table><thead><tr><th width="164">Field of development</th><th width="180">Overseen by</th><th width="248">Developers</th><th>Main languagues</th></tr></thead><tbody><tr><td>Core protocol</td><td>Decentralized ASAP</td><td>RGB core maintainers, but eventually ossified (i.e. no development activity)</td><td>Rust</td></tr><tr><td>Toolchain</td><td>LNP/BP Standards Association</td><td>Association &#x26; member companies</td><td>Rust</td></tr><tr><td>Schemata</td><td>LNP/BP Standards Association</td><td>Independent companies &#x26; developers</td><td>Contractum (alternatively, Rust)</td></tr><tr><td>Smart contracts</td><td>nobody</td><td>Issuers: independent companies, teams, DAOs, issuing assets &#x26; creating smart contracts</td><td>JSON &#x26; any languagues working with Web</td></tr><tr><td>Integration (wallets, exchange etc)</td><td>Integration standards proposed by LNP/BP Standards Asociation</td><td>Applied software companies: exchanges, wallet devs, outsourcers etc</td><td>JavaScript, TypeScript, Python, C, Java, Kotlin, Swift, Rust</td></tr></tbody></table>

Core protocol devs, upon final RGB/1 v1.0 release will perform just the bugfixing.

Toolchain development, managed and sponsored through LNP/BP Standards Association, will continue to produce and improve tools for other developer categories.&#x20;

Schemata development consists of two main tasks:

* Defining standards for API used in most common use cases.
* Develop specific schemata, which may be seen as "RGB smart contract templates created by domain professionals".

The first case is covered by LNP/BP standards. Anybody can propose a new standard for a Schema (these standards are called "Schema (API) standards"). The standards are reviewed by the same process as any other LNP/BP standard, and are overseen by LNP/BP Standards Association quite similar to how IETF oversees Internet standards (RFCs).

Development of a schema confirming to some, multiple - or even none - or Schema Standards can be performed by anybody, independently from LNP/BP Standards Association or any other body. The only requirement - to unserstand how to develop Schema and ability to write them using Contractum languague.&#x20;

LNP/BP Standards Association maintains [registry of the schemata](https://github.com/RGB-WG/schemata), however any other body may create an independent registry, so multiple registries may co-exist. The process of adding an implementation to the LNP/BP registry is very simple: just submit a PR request providing all necessary information about your schemata.

Using schemata, the development of actual smart contracts require no coders and conding: it comes down to the selection of a schema (or multiple schemata) which the contract must confirm to - and filling in the data specific to that schemata in pretty much the same way as filling in paper forms. This is done with some data-oriented languagues, like JSON, YAML, XML - or using some user interface tools supplied by LNP/BP Association or independent companies for existing schemata types (like fungible asstets, NFTs, identity etc).

