# Schema

An RGB Schema defines, through coding, the necessary template for Genesis and embeds all the rules of available [contract operation](../../annexes/glossary.md#contract-operation) representing the [business logic](../../annexes/glossary.md#business-logic) of the contract and which allows for the [state](../../annexes/glossary.md#contract-state) of the contract to be updated.

&#x20;As [mentioned earlier](../schema-interface.md) a Schema RGB is the analogue of a class for an OOP language. Hence such a construction is used to define the various standards for RGB assets, for example: fungible assets, collectibles, digital identities, etc.&#x20;

The [issuer](../../annexes/glossary.md#contract-participant) of a token on RGB uses (and make available to the public)  a Schema in order to define the issuance properties encoded in the Genesis such as that the contract can be supported by wallets and exchanges. Thus, **when wallets and exchanges receive some information about an asset on RGB (data and contract) they must validate them against the Schema used by the issuer of that asset.**&#x20;

In fact the Schema validation is the very first operation step which an user need to undergo before interacting in any way with the contract (e.g. to perform the desired contract operations)&#x20;

From a contract functional point of view, the **Schema construct addresses the following questions**:

* What kinds of owned states and assignments exist?
* What kinds of publicly-executable rights (valences) exist?
* What global state does the contract have?
* How is the genesis contract structured?
* What kind of state transitions and extensions are possible?
* What metadata can contract operations have?
* How state data are allowed to change with state transitions?
* What sequences of transitions are allowed?

## Schema Structure

**From a technical point of vier an RGB Schema is a functional declarative document** that can be written in different programming or markup languages such as: Rust, YAML or JSON. It can also be written in Rust, but the code is then compiled to return only the fields of the data structure and that is how it appears to the user.&#x20;

This is done by defining types for metadata, proper state, global state, valences, and possible combinations of all these types within the different types of state transitions, as well as state genesis and extension. When a very expressive language is needed, being a declarative language, the rules of contract evolution are defined and this covers the vast majority of use cases. However, if you want to have additional validation for which you need something much more expressive, you can use scripts. These can be defined to perform validation for each type of state, depending on the type of state. So, you provide a library, where you provide validation entry points for a certain dataset, a certain type of state transition, a certain state extension, some genesis data, and so on, as necessary. The result of the script execution must be success or failure. The script is able to access the state transition data, the state of the contract as a whole, and in the future access to Bitcoin blockchain (or other sidechains) data and global state will also be added.&#x20;

<figure><img src="../../.gitbook/assets/compiled_schema_structure.png" alt="Compiled Schema Structure"><figcaption><p><strong>General Layout of a Schema. Every schema is marked by a SchemaID referencing the kind of contact being implemented. Follows the declaration of Global and Assignments of owned State Owned States, each one  preceded by its own Type. Then the definition of he Contract Operation and finally the validation script and the strict type system used for all the declarations.</strong> </p></figcaption></figure>



* &#x20;Defines all the variable used in contract state and transition in a [strict-type](https://www.strict-types.org/) fashion.  In particular, Schema contains the `Types` related to:
  * Metadata.
  * Owned state.
  * Global state.
  * Valences (public rights).
  * Contract Operation.
* Defines the requirements needed to validate state transitions outside the Layer 1 (state owned) provided by Bitcoin Script-managed commitments.&#x20;
* Allows for simple updates to the contract without having to modify the software, so that wallets, explorers, and LN nodes can accept new asset types without making any changes to their respective code.&#x20;
* Embeds the state validation functions for the client-side part of RGB executed through the [AluVM](../../annexes/glossary.md#aluvm) engine and which represents most fundamental parts of it's business logic. This kind of validation function, for instance, of possesses the following signature declaration: `validate :: state -> bool`.

**This architecture  is very different from blockchain-based contracts**, for example those  implemented on Ethereum, because in that case **the contract is a executable code** that implements the rules for changing the state and implements the state. I**n contrast, in RGB the contract is purely declarative**.&#x20;



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
