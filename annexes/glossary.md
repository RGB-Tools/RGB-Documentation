---
description: Terminology used in RGB sorted in alphabetical order
---

# Glossary

#### Anchor

Set of client-side data that proof the inclusion of a unique commitment inside a transaction. In RGB protocol it is constituted by:

* The Bitcoin transaction ID
* The [MPC](glossary.md#multi-protocol-commitment---mpc)
* The [DBC](glossary.md#deterministic-bitcoin-commitment---dbc)

#### AluVM

Acronym of Algoritmic logic unit Virtual machine is register-based virtual machine for smart contract validation and distributed computing, used but not limited to RGB contract validation. [link](https://www.aluvm.org/)

#### Assignment

The RGB-equivalent of a transaction output modifying, updating or creating some properties of the state of a [contract](glossary.md#contract). It is formed by a [Seal Definition](glossary.md) and a [Owned State](glossary.md)

#### Client-side Validation

The operation which allows the verification of some data exchanged between parties according to some defined protocol rules. In RGB protocol these data are in form of [consignment](glossary.md#consignment); the above data can be exchanged privately between the parties involved as, unlike Bitcoin protocol, they don't need to be registered on a public medium (e.g. the blockchain).

#### Commitment

Formal timestamped fingerprint expressed as the registration of an hash referring to some structured data over some defined medium expressing time indication and chronological ordering (e.g. the blockchain)

#### Consignment

The data transferred between parties that are subject to client-side validation. There are 2 main types of consignment:

* Contract Consignment: provided by the contract issuer including the main information about the contract
* Transfer Consignment: provided by the payer user party and containing all the state transition history up to the [terminal consignment](glossary.md)

#### Container

The way how [stash](glossary.md#stash) data are exchanged between users.

#### Contract

A set of rights established and executed digitally between certain parties. A contract has state and business logic, expressed in terms of ownership rights and executive rights. The contract state, rights and conditions of valid operations are defined using RGB schema; only state and operations which allowed by the schema declarations and validation scripts are allowed to happen within the contract scope.

#### Contract State

The set of up to date, private and public information and data related to a contract. In RGB the contract state is constituted by:

* Global State
* Owned State

#### Contract Participant

An actor which participate in contract operations. Contract parties are classified into the following categories:

* Contract issuer: an actor creating contract genesis.
* Contract party: all actors which have some ownership rights over RGB contract state.
* Public party: an actor constructing state extensions. Can exist only in contracts providing valencies and state extensions.

#### Deterministic Bitcoin Commitment - DBC

The set of rules which allows for the registration of a provably single [commitment](glossary.md#commitment) in a Bitcoin transaction. Specifically, RGB protocol embeds 2 forms of DBC:

* Opret
* Tapret

#### Directed Acyclic Graph - DAG

A directed graph which do not contains any directed cycle thus allowing topological ordering - [wiki link](https://en.wikipedia.org/wiki/Directed\_acyclic\_graph)

#### Engraving

An optional fingerprint that past owners of a contract can register allowing verification of following users. It is implemented in RGB21 interface.

#### Extra Transaction Proof - ETP

The part of the Anchor which embeds the additional data necessary for the validation of tapret commitment, such as the internal PubKey and the Script Path Spend.

#### Genesis

The set of data, regulated by a contract [schema](glossary.md#schema), which represent the starting state of every contract of RGB. It's the equivalent of Bitcoin Genesis Block in the Client-side level.

#### Global State

A set of public data representing some publicly available information of a contract. Differently from Owned State information they are not assigned to any Bitcoin UTXO, thus owned by anybody.

#### Interface

The set of instructions that allows to transform contract binary data of contracts and schemata in user and wallet-readable information.

### Invoice

A Base58 encoded string, which support URL scheme capabilities, embedding the necessary data in order to allow a payer counterpart to construct a state transition.

#### Multi Protocol Commitment - MPC

The Merkle Tree structure used in RGB to include in a single commitment into the Bitcoin Blockchain multiple contract state transitions of different contracts.

#### Owned State

The Data structure which allows for the specifications of state Data inside an Assignment. Those data, through Seal Definition, are assigned to a specific Bitcoin UTXO which represents the new ownership of the state.

#### Ownership

The control and thus the possibility to spend an UTXO to whom some client-side property are assigned.

#### Schema

The set of rules and business logic according to which an RGB contract works.

#### Seal Definition

#### Shard

A branch of the DAG of the RGB contract transitions

#### Single-Use Seal

A promise to [commit](glossary.md#commitment) to a yet unknown message in the future, once and only once, such that commitment fact will be provably known to all members of a certain audience.

#### Stash

The set of client-side data over which have undergone [validation](../terminology/glossary-of-terms.md#client-side-validation) and are stored by the user.

#### State Extension

A contract operation which allows for the redeeming of some Valencies. It needs to be closed by a State Transition in order to put in effect the changes to the contract expressed by the Valencies

#### State Transition

The most important contract operation which make possible the transition of an RGB State to a New State, changing state data and/or ownership.

#### Taproot

#### Terminal Consignment - Consignment Endpoint

The last state of a contract which include the last state transition constructed from a payee counterpart invoice.

#### Transition Bundle

A set of RGB [State Transition](glossary.md), belonging to the same contract, which are constructed by different parties closing their seal in a single operations.

#### Valency

A public rights having no state but which can be referenced and redeemed through a state extension.
