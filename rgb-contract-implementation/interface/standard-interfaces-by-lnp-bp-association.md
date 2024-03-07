# Standard Interfaces by LNP/BP Association

In this section we will provide some description of the Interface standards developed by [LNP/BP Association](https://www.lnp-bp.org/) and which provide a good starting point to work with RGB. The list is divided  into [already-coded interfaces](https://github.com/RGB-WG/rgb-std/tree/master/src/interface) (ready-to-use) and interface which will be developed in the future.&#x20;

It's important to point out that Interface provide naming to data structure and operation to be used in the wallet or to be visualized by users, but the actual "contract job" is done primarily by the [Schema](../schema/) to which the appropriate interface (or a set of Interfaces) can be connected through the respective Interface Implementation(s). &#x20;

## Ready-to-use interfaces

The following Interfaces are fully compatible and tested to work with RGB consensus and standard libraries.

* **RGB20** is an interface equivalent of ERC20, but actually allows much more than Ethereum's standard. **It is the standard to address the parsing of any fungible asset**: stocks, bonds or, in general, anything that requires fungibility. It can be connected for example to the [Non Inflatable Fungible Asset (NIA)](https://github.com/RGB-WG/rgb-schemata/blob/master/src/nia.rs) contract schema. Among the features that RGB20 has over the ERC20 standard there are:
  * **Asset renaming**, and possibility to change other specifications such as the **ticker**.&#x20;
  * **Stock split**, similar to those of the stock markets, or the possibility to **change the precision** of the token.
  * S**econdary issuance**, which can be unlimited, limited to specific values or unique.&#x20;
  * **Asset burning or replace** by the issuer.  The interface is designed to allow for specific parties to accomplish those task even associated to the issuance of a new contract contemporary to burning actions which make possible the reduction of the size of the contract [stash](../../annexes/glossary.md#stash).
* **RGB21** is the interface which is design to address **NFT contracts, or in general any digital production contract** such as digital media, books, movie, or music etc. It can be connected to the [Unique Digital Asset (UDA)](https://github.com/RGB-WG/rgb-schemata/blob/master/src/uda.rs) contract schema. As interesting additional features it provides:
  * The built-in support for direct fetch of the media file from the contract if its size is below 16MB.
  * The possibility, for the Owner, to register [engraving](../../annexes/glossary.md#engraving) to mark the possession of the asset which remain in the asset's history after it has been sold. This feature is provided in order leverage in direct and in trustless way some notable user's possession in the NFT exchange history.
* **RGB25** represents **an hybrid of RGB20 and RGB21** thus addressing the need to interface **partially fungible asset** contracts.  For instance it is made for assets which need to be fractionated but which need to maintain a relations with the single asset issued in the first place. A typical example would be the use of such interface for real estate tokenized assets. It can be connected to  [Collectible Fungible Asset (CFA)](https://github.com/RGB-WG/rgb-schemata/blob/master/src/cfa.rs) schema.

## Planned interface to be developed

These interfaces haven't been implemented yet.

* **RGB22** is a standard interface meant to **implement digital identities**.&#x20;
* **RGB23** is aimed at implementing a more advanced version of [opentimestamps protocol](https://opentimestamps.org/) with additional features suitable to provide a provable history of the commitments of digital documents.
* **RGB24** addresses the need to interface to contracts which provide a **Decentralized Domain Name System** like Ethereum's ENS.
* **RGB26** represents the RGB **standard for DAOs** which can have complex contract configurations.
* **RGB30** interface concept is very similar to an RGB20 interface, however it is able to connect to contracts which embeds **decentralized issuance**. RGB30 is the only standard that foresee to use [state extensions](../../annexes/glossary.md#state-extension).

In the following section we will report the code of RGB20 interface.

***

