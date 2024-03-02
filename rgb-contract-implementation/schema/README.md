# Schema

From a technical point of view, a Schema defines the requirements needed to validate state transitions outside the authorization level (state owned) provided by Bitcoin Script-managed commitments. It also allows for simple updates to the contract without having to modify the software, so that wallets, explorers, and LN nodes can accept new asset types without making any changes to the code. The Schema is, therefore, the set of validation rules for the client-side part of RGB. The schema may contain Turing-complete scripts that define the business logic for client-side validation. The various objects defined in the script schema are used during validation of state transitions on _AluVM._

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

<figure><img src="../../.gitbook/assets/compiled_schema_structure.png" alt="Compiled Schema Structure"><figcaption><p><strong>Compiled Schema Structure</strong></p></figcaption></figure>
