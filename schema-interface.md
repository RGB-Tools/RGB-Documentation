# Contract building: Schema and Interfaces

We come to how an RGB contract is actually defined and implemented. Its code consists of two independent and complementary components: the _Schema_ and the _Interface_.

A Schema defines a standard/blueprint for the business logic of a contract, in fact it includes the constructor for the genesis state of the contract and for the various transition functions between different states of the contract. We can see it as the RGB analogue of a class for an OOP language or as an ERC standard for Ethereum contracts. It, therefore, is used to define the various standards for RGB assets, for example: fungible assets, collectibles, digital identities, etc...
The issuer of a token on RGB uses a Schema to define the issuance contract so that it is supported by wallets and exchanges. Thus, when wallets and exchanges collect information about an asset on RGB (data and contract) they must validate it against the Schema used by the issuer of that asset. Only if the Schema validation is successful, i.e., does not fail, can the contract status transition requested by the user be made.

An RGB Interface represents a standardized way to define an API for smart contracts. It can be compared to the interfaces of various OOP languages such as Java, but also to traits in Rust, or to the ABIs and ERC standards of smart contracts on Ethereum. However, it differs from Ethereum's ABIs in that they are always included in the contract. Through its use, wallets and other software can provide users with a semantically aware user interface for contract processing. In addition, contract developers can add other interfaces to existing contracts without having to update the contracts themselves (which are immutable).

From the above, it is clear that since Schema and Interface are two quite distinct things that can be developed independently, then there must be a way for them to interact. This is what is called _implementing an interface_ for a given Schema. It is for all intents and purposes a map between schema and interface that is mediated by the use of the _strict type system_. An implementation can be compared to Rust's concept of impl for structs.

<figure style="text-align: center;">

  <img src=".gitbook/assets/contract_anatomy.png" alt="RGB contract anatomy" style="max-width: 80%; height: auto;">

  <figcaption style="text-align: center;"><p><strong>The code components of an RGB contract</strong></p></figcaption>

</figure>

## Internal mechanics of a Schema

From a technical point of view, a Schema defines the requirements needed to validate state transitions outside the authorization level (state owned) provided by Bitcoin Script-managed commitments. It also allows for simple updates to the contract without having to modify the software, so that wallets, explorers, and LN nodes can accept new asset types without making any changes to the code. The Schema is, therefore, the set of validation rules for the client-side part of RGB. The schema may contain Turing-complete scripts that define the business logic for client-side validation. The various objects defined in the script schema are used during validation of state transitions on _AluVM_.

In RGB the Schema is always defined by the issuer in the genesis state. In it, the following are defined descriptively/functionally:

* the _types_ for
  * metadata (and restrictions on their values);
  * owned state;
  * global state;
  * valences (public rights);
  * possible combinations of the above via state transitions.
* State validation functions (executed by AluVM), i.e., functions that have type-signatures of the type `validate :: state -> bool`, for each data type and operation.

This is very different from blockchain-based contracts, for example smart contracts on Ethereum, because in that case the contract is a code that implements the rules for changing the state and implements the state. In contrast, in RGB the contract is purely declarative. A Schema is a functional declarative document that can be written in YAML or JSON. It can also be written in Rust, but the code is then compiled to return only the fields of the data structure and that is how it appears to the user. This is done by defining types for metadata, proper state, global state, valences, and possible combinations of all these types within the different types of state transitions, as well as state genesis and extension. When a very expressive language is needed, being a declarative language, the rules of contract evolution are defined and this covers the vast majority of use cases. However, if you want to have additional validation for which you need something much more expressive, you can use scripts. These can be defined to perform validation for each type of state, depending on the type of state. So, you provide a library, where you provide validation entry points for a certain dataset, a certain type of state transition, a certain state extension, some genesis data, and so on, as necessary. The result of the script execution must be success or failure. The script is able to access the state transition data, the state of the contract as a whole, and in the future access to Bitcoin blockchain (or other sidechains) data and global state will also be added. Thus, a Schema functionally answers the following questions:

* What kinds of owned states and assignments exist?
* What kinds of publicly-executable rights (valences) exist?
* What global state does the contract have?
* How is the genesis contract structured?
* What state transitions and extensions are possible?
* What metadata can contract operations have?
* How is state data allowed to change with state transitions?
* What sequences of transitions are allowed?

Schema clearly differentiates contract developers from issuers, who know nothing about coding and programming. This is important because it allows the creation of "template contracts" while avoiding common mistakes for issuers.

An RGB contract template defines:

* what types of states can exist;
* the types of data used in the state;
* what operations can be performed with the contract;
* the scripts and validation rules (as, for example, _the algebraic sum of the values of the outputs must equal the algebraic sum of the inputs_).

In summary:

```
RGB Schema <- State data Types + Operation types + Graph evolution rules + Used strict type libs + AluVM validation code
```

## Example of the code of a RGB20 Schema

Let's see what the Schema looks like in case we want to define it via some Rust code. Let's take as an example the [Schema in the RGB repository for fungible non-inflationary assets](https://github.com/RGB-WG/rgb-schemata/blob/master/src/nia.rs) that are something analogous to Ethereum's ERC20 standard.

We see that the `nia_schema()` function has an output of type `SubSchema`, because with a Schema you can have one level of inheritance. So you can have a generic Schema that does many useful things, but you don't want all of them. You want to have something simpler and you can limit the things it can do and create a sub-Schema as a subset of the more generic Schema, providing additional guarantees. So it is a very specific form of inheritance.

{% code fullWidth="true" %}
```rust
fn nia_schema() -> SubSchema {
    // definitions of local variables

    Schema {
        ffv: zero!(),
        subset_of: None,
        type_system: types.type_system(),
        global_types: tiny_bmap! {
            GS_NOMINAL => GlobalStateSchema::once(types.get("RGBContract.DivisibleAssetSpec")),
            GS_DATA => GlobalStateSchema::once(types.get("RGBContract.ContractData")),
            GS_TIMESTAMP => GlobalStateSchema::once(types.get("RGBContract.Timestamp")),
            GS_ISSUED_SUPPLY => GlobalStateSchema::once(types.get("RGBContract.Amount")),
        },
        owned_types: tiny_bmap! {
            OS_ASSET => StateSchema::Fungible(FungibleType::Unsigned64Bit),
        },
        valency_types: none!(),           
        genesis: GenesisSchema {                             //  +---
            metadata: Ty::<SemId>::UNIT.id(None),            //  |
            globals: tiny_bmap! {                            //  |
                GS_NOMINAL => Occurrences::Once,             //  |  (1) Genesis Definition with variables
                GS_DATA => Occurrences::Once,                //  |
                GS_TIMESTAMP => Occurrences::Once,           //  |
                GS_ISSUED_SUPPLY => Occurrences::Once,       //  +---
            },
            assignments: tiny_bmap! {
                OS_ASSET => Occurrences::OnceOrMore,
            },
            valencies: none!(),
        },
        extensions: none!(),
        transitions: tiny_bmap! {
            TS_TRANSFER => TransitionSchema {
                metadata: Ty::<SemId>::UNIT.id(None),
                globals: none!(),
                inputs: tiny_bmap! {
                    OS_ASSET => Occurrences::OnceOrMore
                },
                assignments: tiny_bmap! {
                    OS_ASSET => Occurrences::OnceOrMore
                },
                valencies: none!(),
            }
        },
        script: Script::AluVM(AluScript {
            libs: confined_bmap! { alu_id => alu_lib },
            entry_points: confined_bmap! {
                EntryPoint::ValidateGenesis => LibSite::with(FN_GENESIS_OFFSET, alu_id),
                EntryPoint::ValidateTransition(TS_TRANSFER) => LibSite::with(FN_TRANSFER_OFFSET, alu_id),
            },
        }),
    }
}
```
{% endcode %}

After defining the generic `Schema`, if any, to which the Schema you are defining belongs, you define the data type system you are using, `type_system`. This comes from the standard types provided by strict types, `StandardTypes`, extended with `Rgb20`, which is the RGB equivalent of the ERC20 standard, i.e. the standard data type for fungible assets. This data type includes such things as the quantity of tokens, the date and time of issue, the asset specification, i.e., the Rust structure containing the name and precision of the asset. Everything is compiled from the strict types. Whereas in Ethereum, to create a contract that does not allow the ticker to have more than eight characters, we have to write code, for example with Solidity, take the string that contains the ticker, measure the number of characters and consume gas in the process, consuming computing power, in RGB we do not write code. We provide the definition of the restrictions and the type system level. Then we specify that the contract can have a global type which is the token name. And this token name, for its type, is restricted. It has to be longer than one character, but no longer than eight, and each one has to be an ASCII character, and we do this without any scripting, but just using the type system. So we can say that RGB implements functional smart contracts. So we define the global data type `global_types` within which we can define, for example, the nominal. So we can have a nominal value as part of the state and we can have it only once, that is, once it is updated, the last one is discarded. So it is mutable, not accumulable. And it comes from the data type specific structure, which is asset specific. It is a type specification, which has all these fields. So when we rename the assets, we define all these fields. Among other global types we can have: timestamp, total number, supply information and so on. Then we can have a type of `owned_types` which in the example must be a 64-bit unsigned fungible quantity, `FungibleType::Unsigned64Bit`. In the example there is no valency type, `valency_types` is `none`. So this is a very simple scheme, which does not allow us to create secondary emissions, and we can declare it at the scheme level, instead of writing the code in the contract. We can therefore define genesis, transition, and extensions. Genesis can contain metadata, but in this case it does not contain it because we used the unit type, which is always empty data. Also, we notice that in this case there is only one type of state transition, which is transfer. And this transfer, again, has no metadata. It does not define any new global data type. It can only have one type of input, which is a previously owned asset. It can refer to multiple previously owned assets. It can also create new assignments of the type of resource owned, even one or more. And that's it. There is a small validation script with the flood that has only one entry point, validate its own state. This script verifies that the sum of the inputs of the Pedersen commitments is equal to the sum of the outputs of the Pedersen commitments. The power of RGB is that you don't actually have to write the contract this way, because you can write the same thing using YAML or JSON, using the serializer/deserializer to serialize it into the schema object.

## Smart Contract Operations and compiled Schema structure

Recall from the previous chapter that the operations of a smart contract can be divided into state generation and state transition events under a single contract grouped together by a specific finality proof (anchor). More specifically we have:

* State generation:
  * genesis;
  * state extension.
* State transition.

Within a contract the state is structured into:

* _**metadata**_ ("local" state of the transaction);
* _**assignment**_, which consist of.
  * types of property rights (from the schema);
  * definition of the Single-Use-Seal owning that right;
  * state data (optional).
* _**assignments**_: public rights (from the schema) without state. Anchor points for _state extensions_.

The following table shows how the status can be updated by different types of operations:

|                   | Genesis | State Extension | State Transition |
| ----------------- | :-----: | :-------------: | :--------------: |
| Metadata          |    +    |        +        |         +        |
| Valences          |    +    |        +        |         +        |
| Assignments       |    +    |        +        |         +        |
| Input             |    No   |        No       |         +        |
| Redeemed Valences |    No   |        +        |        No        |

Below is the general structure of the schema when it is compiled. We can see that it contains a reference to the main schema. It contains the sections about the structure of the schema. It contains the status types: global, assignment and valence. Contains the section on contract operations. Defines different types of transitions and extensions. Genesis type. Each defines rules for updating states. Finally, the strict type system and validation scripts for specific state types and state transitions.

<figure style="text-align: center;">

  <img src=".gitbook/assets/compiled_schema_structure.png" alt="Compiled Schema Structure" style="max-width: 80%; height: auto;">

  <figcaption style="text-align: center;"><p><strong>Compiled Schema Structure</strong></p></figcaption>

</figure>

## Interfaces

We anticipated that an interface is both human-readable and wallet-readable information about the contract, the state it is in, and the transactions it can make. The wallet can interact with different contracts using interfaces. So the only thing the wallet has to learn is not the billions of pattern shapes, which can happen, but a small amount of interfaces, which are commonly used. And the interfaces can have a little bit of functionality. They don't necessarily have to cover everything. For example, you can have an interface for a named contract, which just returns the name of the contract or something like that. So it is a fairly composite thing, and the contract can have multiple interfaces to the outside world, which makes things much simpler.

<figure style="text-align: center;">

  <img src=".gitbook/assets/interfaces.png" alt="Interfaces" style="max-width: 80%; height: auto;">

  <figcaption style="text-align: center;"><p><strong>Example of a wallet that interacts with multiple contracts through various interfaces</strong></p></figcaption>

</figure>

They, therefore, make sense of the different contracts for the user, telling the wallet, first of all, what state the contract has. In addition to the semantic meaning of the state they also provide information on how to parse that state. The only thing the wallet gets through the interface, if you are working with RGB from outside Rust, is a JSON (or YAML) structure, which is self-explanatory, with field names and everything, so that it is easy to make sense of the internal structured data, even if it is complex structures. In addition, the interface tells the wallet what operations can be performed with the contract, what arguments it accepts. Because each argument is structured data, a wallet can also have a way to expose any interface because from the structured data you can generate a form. This means that RGB basically support any smart contract with any interface because of this explanatory layer.

So, a contract can implement many interfaces to provide advanced functionality, and you can update the functionality of the contract and have users be able to use it without asking the wallet developers to update their software. So, for example, suppose you exposed some of it through the standard interface such as RGB20. Unlike Ethereum's ERC20 standard, the contract is created without a single transaction on the blockchain. In fact, you just fill out the form and create a binary object that you then send to other people. So, you can do that and people will see, you will see 20 interfaces in their wallets when they import your contract, but the day after tomorrow you could create a new interface that exposes some other part of the functionality, send it to your users and they will immediately see more of your contract in their wallet without the wallet developers updating or making a new release. What the interface does is it takes the name, then it defines the set of states, like it knows the sum of the states of the contract, and it says these contract-specific state types have these names, and these data types are also bound to the strict type definition. So you basically add semantics to what is already in the contract, and the same thing happens with operations and arguments. So, the interface is a very, very small thing. It's just two mappings.

<figure style="text-align: center;">

  <img src=".gitbook/assets/interface_anatomy.png" alt="Interface anatomy" style="max-width: 80%; height: auto;">

  <figcaption style="text-align: center;"><p><strong>Components of an RGB interface</strong></p></figcaption>

</figure>

## Interfaces by LNP/BP Association

There are a number of things that are quite common and that is why the LNP/BP association has published (or will publish) them as a default set. Of course, over time it is possible that more will be added. These standards include:
* **RGB20**: is an equivalent of ERC20, but actually allows you to do much more than you can do with ERC20. It is the standard for any fungible asset: stocks, bonds or, in general, anything you want/can make fungible. Among the features that RGB20 has over the ERC20 standard, we have, first, that you can rename the asset, change its data and ticker. You can also do what is called a stock split in the stock market or simply change the precision of the contract. Another thing you can do is secondary issuance, which can also be limited. That is, you can create a contract that says secondary issuance is not possible and the user will know that. Or you can create a contract that says that secondary issuance is possible up to a certain amount and these are the parties who have the right to make this issuance. By the time they issue, this UTXO will be spent and you will know that the bid has increased. Or, you can have an asset that says it has an indefinite issuance. Or, you can have an asset that has zero initial issuance and delegates issuance for a certain period of time. So, the possibilities are many. The other thing you can do is burn the asset or replace it by the issuer. You can also allow replacement of assets to certain parties, so that people who want to reduce the size of their history can go to the party and send the current status and receive a new contract, the same token with the same contract ID. But again, if you don't want that, you can limit the functionality and have a very secure token, where people are not afraid that you will reissue more and more tokens, because you could not reissue more and more tokens with the same contract.
* **RGB21**: which is a type of NFT, but it's not just an NFT. You can think of it as a digital production contract. An author creates a digital media, or a book, or a movie, or music, or whatever he wants to create, and reissues an RGB21 contract. The know-how of this contract prevents anyone from stealing anything. If someone wants to steal something, they have all the options to do so, as they can do with JPEGs in NFT, which is what NFT is today. However, for those who want to, not steal, but pay for, support something, they have a way to prove the fact of history, or pass it on to future owners, and it is basically a digital certificate of ownership of a certain object, which can be divided, so that it is not fungible between parties, so it can be divided into multiple objects. You can have a collection of non-fungible things, but each of them can be divided, so you can have multiple owners owning a share of an indivisible thing. The other interesting thing it does is that, unlike Ethereum, it holds the media file. As long as it is less than 16 megabytes, the file is included in the submission and is passed along. If it's greater than 16 megabytes, we don't want to pass terabytes of consignment, it would take too long between wallets, so it defers to an external medium where you can download the file. Also, RGB21 includes the ability to do things called etchings, which you can enable; by default they are not there, but with etchings you can add media on top of media even if you are not the creator of the non-fungible asset. So you can have an image and then have anyone put a signature on that image. The user interface of the portfolio will be able to show that there is an image, but there is also a history of engravings by previous owners. You can then raise the price of an object, for example, someone's digital media, an image, and then pass it on to a famous soccer player who put a signature on it, sold it for a higher price, and so on. So you can make all these games.
* **RGB22**: this is a way to implement a digital identity. You can add meta-information about your identity. You can hide parts of this meta-information from different parties, using the hidden methods. You can distribute this information through dispatches and everything else. You can also create a set of related facts and a history of related facts, such as some people with other identities have signed your identity due to the fact that you are over 21 years old. And you can decide whether or not to use that fact or hide it. So you have a whole infrastructure for digital identity management on top of the public key and the revocation primitive. Basically, you can have an infrastructure for managing self-serving identity.
* **RGB23**: It's an open timestamp on steroids, which means that now it's not just about proving that you knew something in the past, but you can have a demonstrable history. For example, if you are a lawyer, you can have a demonstrable history of certain events. Or if you are a doctor, a hospital, you have a record of things that has to be immutable, that you cannot correct backwards. You don't need blockchain for that. You don't need to go on Hyperledger or anything like that, but you can use RGB on top of Bitcoin, inheriting Bitcoin's resistance to decentralized censorship and Bitcoin's security for immutability. Because if you run Hyperledger on your servers, you don't actually have immutability, despite it being a blockchain. Because your sysadmin can simply block history. And that's not possible here. You store everything on the client side, not on the blockchain. It's all private and you can expose it, reveal it whenever you need it, in the form you need it and the part you need it.
* **RGB24**: which is something that Ethereum namespace, the Ethereum naming system, tried to create. Basically it could become an alternative to DNS. It is the way you can build a global namespace registry, again, without creating new blockchains like Namecoin, without putting data on blockchains like Ethereum, and so on.
* **RGB25**: is a hybrid of RGB20 and RGB21, that is, a partially fungible asset. Basically, if you have, for example, a property and you can create a contract that contains information about the property, it will be fungible because of the divisibility within the property, but each piece will still have some relationship to a real physical object, a part of the real physical object. This can then be useful for tokenization of a real-world asset. This, of course, does not mean that the contract imposes something in the real world from the digital world, but, if the parties are collaborative, they now have a privacy-based means of resisting censorship to account for the things they own in the real world. And again, if you link it to economic incentives, to some other Bitcoin financial contract, you can also build an economic incentive to follow the rules that have been defined here.
* **RGB26**: is a standard for DAOs, but it will work very differently from DAOs already seen on other protocols. Basically, the DAO is a dynamic set of multisigs. So it is a multisig, but unlike the multisig, it is dynamic. With RGB26 You can pass the right to vote without making a transaction on the chain. So you can put this DAO into a Lightning channel and run it there, and this DAO will maintain the state of this multisig for you. But the other thing you can do is you can also have the provable history of the decisions made by that DAO in the form of RGB, what was it, RGB23. So the same probable history of the decisions made and who voted on them.
* **RGB30**: It is very similar to an RGB20 asset, but it is issued in a decentralized way. RGB30 is the only standard that uses state extensions at the current state of development.

These interfaces are available in the standard RGB library, but anyone can develop alternative or additional interfaces.

## Example code of an RGB20 interface with related implementation

Let's take a closer look at what the Rust code of an interface looks like by taking the example of [standard RGB20](https://github.com/RGB-WG/rgb-std/blob/master/src/interface/rgb20.rs).

```Rust
fn rgb20() -> Iface {
    let types = StandardTypes::with(rgb20_stl());

    Iface {
        version: VerNo::V1,
        name: tn!("RGB20"),
        global_state: tiny_bmap! {
            fname!("spec") => GlobalIface::required(types.get("RGBContract.DivisibleAssetSpec")),
            fname!("data") => GlobalIface::required(types.get("RGBContract.ContractData")),
            fname!("created") => GlobalIface::required(types.get("RGBContract.Timestamp")),
            fname!("issuedSupply") => GlobalIface::one_or_many(types.get("RGBContract.Amount")),
            fname!("burnedSupply") => GlobalIface::none_or_many(types.get("RGBContract.Amount")),
            fname!("replacedSupply") => GlobalIface::none_or_many(types.get("RGBContract.Amount")),
        },
        assignments: tiny_bmap! {
            fname!("inflationAllowance") => AssignIface::public(OwnedIface::Amount, Req::NoneOrMore),
            fname!("updateRight") => AssignIface::public(OwnedIface::Rights, Req::Optional),
            fname!("burnEpoch") => AssignIface::public(OwnedIface::Rights, Req::Optional),
            fname!("burnRight") => AssignIface::public(OwnedIface::Rights, Req::NoneOrMore),
            fname!("assetOwner") => AssignIface::private(OwnedIface::Amount, Req::NoneOrMore),
        },
        valencies: none!(),
        genesis: GenesisIface {
            metadata: Some(types.get("RGBContract.IssueMeta")),
            global: tiny_bmap! {
                fname!("spec") => ArgSpec::required(),
                fname!("data") => ArgSpec::required(),
                fname!("created") => ArgSpec::required(),
                fname!("issuedSupply") => ArgSpec::required(),
            },
            assignments: tiny_bmap! {
                fname!("assetOwner") => ArgSpec::many(),
                fname!("inflationAllowance") => ArgSpec::many(),
                fname!("updateRight") => ArgSpec::optional(),
                fname!("burnEpoch") => ArgSpec::optional(),
            },
            valencies: none!(),
            errors: tiny_bset! {
                SUPPLY_MISMATCH,
                INVALID_PROOF,
                INSUFFICIENT_RESERVES
            },
        },
        transitions: tiny_bmap! {
            tn!("Transfer") => TransitionIface {
                optional: false,
                metadata: None,
                globals: none!(),
                inputs: tiny_bmap! {
                    fname!("previous") => ArgSpec::from_non_empty("assetOwner"),
                },
                assignments: tiny_bmap! {
                    fname!("beneficiary") => ArgSpec::from_non_empty("assetOwner"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    NON_EQUAL_AMOUNTS
                },
                default_assignment: Some(fname!("beneficiary")),
            },
            tn!("Issue") => TransitionIface {
                optional: true,
                metadata: Some(types.get("RGBContract.IssueMeta")),
                globals: tiny_bmap! {
                    fname!("issuedSupply") => ArgSpec::required(),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_non_empty("inflationAllowance"),
                },
                assignments: tiny_bmap! {
                    fname!("beneficiary") => ArgSpec::from_many("assetOwner"),
                    fname!("future") => ArgSpec::from_many("inflationAllowance"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    SUPPLY_MISMATCH,
                    INVALID_PROOF,
                    ISSUE_EXCEEDS_ALLOWANCE,
                    INSUFFICIENT_RESERVES
                },
                default_assignment: Some(fname!("beneficiary")),
            },
            tn!("OpenEpoch") => TransitionIface {
                optional: true,
                metadata: None,
                globals: none!(),
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("burnEpoch"),
                },
                assignments: tiny_bmap! {
                    fname!("next") => ArgSpec::from_optional("burnEpoch"),
                    fname!("burnRight") => ArgSpec::required()
                },
                valencies: none!(),
                errors: none!(),
                default_assignment: Some(fname!("burnRight")),
            },
            tn!("Burn") => TransitionIface {
                optional: true,
                metadata: Some(types.get("RGBContract.BurnMeta")),
                globals: tiny_bmap! {
                    fname!("burnedSupply") => ArgSpec::required(),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("burnRight"),
                },
                assignments: tiny_bmap! {
                    fname!("future") => ArgSpec::from_optional("burnRight"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    SUPPLY_MISMATCH,
                    INVALID_PROOF,
                    INSUFFICIENT_COVERAGE
                },
                default_assignment: None,
            },
            tn!("Replace") => TransitionIface {
                optional: true,
                metadata: Some(types.get("RGBContract.BurnMeta")),
                globals: tiny_bmap! {
                    fname!("replacedSupply") => ArgSpec::required(),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("burnRight"),
                },
                assignments: tiny_bmap! {
                    fname!("beneficiary") => ArgSpec::from_many("assetOwner"),
                    fname!("future") => ArgSpec::from_optional("burnRight"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    NON_EQUAL_AMOUNTS,
                    SUPPLY_MISMATCH,
                    INVALID_PROOF,
                    INSUFFICIENT_COVERAGE
                },
                default_assignment: Some(fname!("beneficiary")),
            },
            tn!("Rename") => TransitionIface {
                optional: true,
                metadata: None,
                globals: tiny_bmap! {
                    fname!("new") => ArgSpec::from_required("spec"),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("updateRight"),
                },
                assignments: tiny_bmap! {
                    fname!("future") => ArgSpec::from_optional("updateRight"),
                },
                valencies: none!(),
                errors: none!(),
                default_assignment: Some(fname!("future")),
            },
        },
        extensions: none!(),
        error_type: types.get("RGB20.Error"),
        default_operation: Some(tn!("Transfer")),
        type_system: types.type_system(),
    }
}
```

From Rust code an interface looks very similar to a Schema, but the key difference is that the types are defined in terms of strings, rather than Rust's primitive data types, which are connected directly to the strict data types, see `RGBContract`, that define the semantics for the API. See for example the various transition functions that have meaningful names such as `Transfer`, `Issue` etc... with their equally easily interpretable input arguments such as `input`, `used` etc... which have a data structure of type `assetOwner` defined in the interface itself in a declarative manner. The interface also declares its own error type, `error_type`, and default operation, `default_operation`, which in this case is `Transfer`. Note that, unlike a Schema, in an interface we do not have any AluVM code, since the purpose of the interface does not consist of the business logic of the contract, as mentioned earlier.

Finally we have the [interface implementation](https://github.com/RGB-WG/rgb-schemata/blob/master/src/nia.rs)

```Rust
fn nia_rgb20() -> IfaceImpl {
    let schema = nia_schema();
    let iface = Rgb20::iface();

    IfaceImpl {
        version: VerNo::V1,
        schema_id: schema.schema_id(),
        iface_id: iface.iface_id(),
        script: none!(),
        global_state: tiny_bset! {
            NamedField::with(GS_NOMINAL, fname!("spec")),
            NamedField::with(GS_DATA, fname!("data")),
            NamedField::with(GS_TIMESTAMP, fname!("created")),
            NamedField::with(GS_ISSUED_SUPPLY, fname!("issuedSupply")),
        },
        assignments: tiny_bset! {
            NamedField::with(OS_ASSET, fname!("assetOwner")),
        },
        valencies: none!(),
        transitions: tiny_bset! {
            NamedType::with(TS_TRANSFER, tn!("Transfer")),
        },
        extensions: none!(),
    }
}
```
We see that the implementation takes the Schema, `nia_schema()`, and Interface, `Rgb20::iface()`, and commits them to the id: `schema.schema_id()` and `iface.iface_id()`. Also, we can see how in effect the implementation maps the types defined by the Schema into the types defined in the Interface via the strict types, e.g. `GS_NOMINAL` into `spec`, `GS_DATA` into `data`, etc...

## Schema workflow

In a previous section it was stated that by virtue of its characteristic of being a blueprint for contracts on RGB a Schema will be written by someone and will be used later by someone else not necessarily capable of programming. The workflow for writing a Schema is as follows:

1. Selection of existing standard Schema on RGB, libraries for strict encoding types and built-in verification procedures or AluVM libraries.
2. Writing the type system in Strict (type language for defining data types and their serialization).
3. Write the necessary validation logic using either Rust in RGB Core, or AluVM with assembly language or ParselTongue (under development).
4. Write a new Schema (root Schema and subschemata) in the _**Contractum**_ language, using interfaces imported from the standard RGB schema library, Strict type system libraries (including those created in p. 2), and the validation procedure from p. 2.
5. Compile the Schema and other libraries created from scratch in binary format, which will provide binaries and symbol files for RGB (used in debugging and package distribution for wallet/exchange developers), strict encoding, and AluVM.
6. Prepare a manifest file that will contain developer information, necessary certificates, and information to create a package containing all the required Schema information and libraries that can be distributed to the wallet, exchange developers, and smart contract issuers (via Bifrost or other means).
7. Run the RGB packaging tool to sign all libraries and place them in the package, upload them to the Storm network and other centralized package managers.
