# Features of RGB State

## Strict Type System

As described in the previous sections, the [state](../annexes/glossary.md#contract-state) represents a set of conditions that are subjected to validation against both the [business logic](../annexes/glossary.md#business-logic) and ordered history of commitments.

In RGB, this data set is actually an **arbitrary rich data set** that:

* are **strongly typed**, meaning that **each variable has a clear type definition (e.g. u8) and lower and upper bounds**;
* can be **nested**, meaning that a type can be constructed from other types;
* can be organized in `lists`, `sets` or `maps`.

To properly encode data in the state in a reproducible way, a [Strict Type System](https://www.strict-types.org/) has been adopted in RGB along with [Strict Encoding](https://github.com/rust-amplify/rust-amplify). This means that:

* Encoding of the data is done according to a precise [schema](features-of-rgb-state.md#terminilogy/glossary.md#schema) which, unlike JSON or YAML, defines a precise structure and layout of the data, thus also allowing deterministic ordering of each data element.
* The ordering of elements within each collection (i.e., in lists, sets or maps) is also deterministic.
* Bounds (lower and upper) are defined for each variable and for the number of elements in a collection (the so called **Confinement**).
* All data fields are byte-aligned.
* Data serialization and hashing are performed deterministically (Strict Encoding) allowing **reproducible commitments** of the data to be created regardless of the system on which that operation is performed.
* Data creation according to the schema is **performed through a simple description language which compiles to binary form** from the Rust Language. Extension to other languages will be supported in the future.
* In addition, compilation according to the Strict Type System produces two types of output:
  * A **compile-time Memory Layout**.
  * **Semantic identifiers** associated with memory layout (i.e., the commitment to the name of each data field).
    For instance, this type of construction is able to make detectable the change of a single variable name, which **doesn't change the memory layout** but **changes the semantics**.
* Finally, Strict Type System allows for **versioning** of the compilation schema, thus enabling the tracking of consensus changes in contracts and the compilation engine.

As a matter of fact, Strict Encoding is defined both at an extremely pure functional level (thus far away from object-oriented programming (OOP) philosophy) and at a very low level (almost a hardware definition, thus far removed from more abstract structures and languages).

### Size limitation

Regarding **data participating in state validation**, the RGB protocol consensus rule applies a **maximum size limit** of 2^16 bytes (64 KiB):

* To the size of **any type of data** participating in state validation (e.g. a maximum of 65536 x `u8`, 32768 x `u16`, etc...)
* To the **number of elements of each collection** employed in state validation. This is designed to:
  * Avoid unlimited growth of client side-validate data per each state transition.
  * Ensure that this size fits the register size of a particular virtual machine [AluVM](state-transitions.md) that is capable of performing complex validations along with RGB.

## The Validation != Ownership Paradigm in RGB

One of the most important features of RGB compared to most blockchain-based smart contract systems is based on the **clear separation between the validation task and ownership** that are defined by the protocol at the most fundamental level.

![](../.gitbook/assets/validation-ownership-1.png)

In practice:

* The **Validation** task, performed by users and observers of the protocol, ensures **how the properties of a smart contract can change** and thus the internal consistency and adherence of state transitions to the smart contract rule. This process is fully realized by the [RGB-specific](../annexes/rgb-library-map.md) libraries.
* The **Ownership** property, which, through the definition of the seal pointing to a Bitcoin UTXO, **defines who can change the state**. The security level of this property depends entirely on the security model of Bitcoin itself.

This type of separation **prevents the possibility of mixing the non-Turing complete capabilities of smart contracts with the public access to contract states** that is embedded in almost all blockchains with advanced programming capabilities. In contrast, **the use of these common "mixed" architectures has led to frequent and notable hacks** in which yet unknown vulnerabilities of smart contracts have been exploited by publicly accessing the contract state encoded in the blockchain.

Moreover, based on Bitcoin's transaction structure, RGB can exploit the **features of the Lightning Network** directly.

## RGB Consensus Changes

As another important feature, RGB has, in addition to Semantic Versioning of data, a **Consensus Update System**, which tracks changes in consent in contracts and contractual transactions. There are basically two ways to update the consent rule embedded in the protocol:

### **Fast-forward**&#x20;

A **fast-forward** update occurs when _some previously invalid rule becomes valid_. Despite the similarities, this kind of update is **NOT comparable to a blockchain hardfork**. The chronological history of this kind of changes is mapped into the contract through the [Ffv field](features-of-rgb-state.md#components-of-a-contract-operation) of Contract Operation. Specifically, it is characterized by the following properties:

* Existing owners are not affected.
* New beneficiaries must upgrade their wallets.

### Push-back

A **push-back** update occurs when _some previously valid state becomes invalid_. Despite the similarities, this kind of update is **NOT comparable to a blockchain softfork**, and furthermore:

* Existing owners can lose assets if they update the wallet.
* It's actually a new protocol, no longer the same version of RGB.
* Can only occur through issuers reissuing assets on a new protocol and users using two wallets (for both the old and new protocols).

## RGB Contract Operation Libraries

Repository:

* https://github.com/RGB-WG/rgb-core which contains all the engine for contract construction and validation.