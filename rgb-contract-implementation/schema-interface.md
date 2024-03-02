# Contract Implementation in RGB

Eventually, we shall come to this final  section in which we will be **describing how an RGB contract is actually defined and implemented**. In addition to [Genesis](../annexes/glossary.md#genesis),  which we have discussed [earlier](../rgb-state-and-operations/state-transitions.md#genesis), the definition of  [contract](../annexes/glossary.md#contract) in RGB ecosystem it is realized by  2  independent and complementary components (in addition to a component, [Interface Implementation](../annexes/glossary.md#interface-implementation), which bridges them):&#x20;

* [Schema](../annexes/glossary.md#schema)&#x20;
* [Interface](../annexes/glossary.md#interface)&#x20;

<figure><img src="../.gitbook/assets/contract_anatomy.png" alt="RGB contract anatomy"><figcaption><p><strong>The list of components which defines a contract in RGB</strong></p></figcaption></figure>



A Schema defines a standard/blueprint for the business logic of a contract, in fact it includes the constructor for the genesis state of the contract and for the various transition functions between different states of the contract. We can see it as the RGB analogue of a class for an OOP language or as an ERC standard for Ethereum contracts. It, therefore, is used to define the various standards for RGB assets, for example: fungible assets, collectibles, digital identities, etc... The issuer of a token on RGB uses a Schema to define the issuance contract so that it is supported by wallets and exchanges. Thus, when wallets and exchanges collect information about an asset on RGB (data and contract) they must validate it against the Schema used by the issuer of that asset. Only if the Schema validation is successful, i.e., does not fail, can the contract status transition requested by the user be made.

An RGB Interface represents a standardized way to define an API for smart contracts. It can be compared to the interfaces of various OOP languages such as Java, but also to traits in Rust, or to the ABIs and ERC standards of smart contracts on Ethereum. However, it differs from Ethereum's ABIs in that they are always included in the contract. Through its use, wallets and other software can provide users with a semantically aware user interface for contract processing. In addition, contract developers can add other interfaces to existing contracts without having to update the contracts themselves (which are immutable).

From the above, it is clear that since Schema and Interface are two quite distinct things that can be developed independently, then there must be a way for them to interact. This is what is called _implementing an interface_ for a given Schema. It is for all intents and purposes a map between schema and interface that is mediated by the use of the _strict type system_. An implementation can be compared to Rust's concept of impl for structs.



##



##

##



##
