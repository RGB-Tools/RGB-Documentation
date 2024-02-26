---
description: Terminology used in RGB sorted in alphabetical order
---

# Glossary

#### Anchor

Set of client-side data that proof the inclusion of a unique commitment inside a transaction. In RGB protocol it is constituted by:

* The Bitcoin transaction ID of the [witness transaction](#).
* The [MPC](glossary.md#multi-protocol-commitment---mpc)
* The [DBC](glossary.md#deterministic-bitcoin-commitment---dbc)
* The [ETP](#extra-transaction-proof---etp) in case of [Tapret](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md) commitment scheme.

#### AluVM

Acronym of Algoritmic logic unit Virtual machine is register-based virtual machine for smart contract validation and distributed computing, used but not limited to RGB contract validation. [link](https://www.aluvm.org/)

#### Assignment

The RGB-equivalent of a transaction output modifying, updating or creating some properties of the state of a [contract](#contract). It is formed by:
 * A[Seal Definition](#seal-definition) 
 * An [Owned State](../rgb-state-and-operations/components-of-a-contract-operation.md#owned-states)

 [Link](../rgb-state-and-operations/components-of-a-contract-operation.md#assignments-of-an-owned-state)

#### Business Logic

The set of operation and rules contained in a contract [Schema](#schema) which allows for the rightful update of the [contract state](#contract-state).

#### Client-side Validation

The operation which allows the verification of some data exchanged between parties according to some defined protocol rules. In RGB protocol these data are in form of [consignment](#consignment); the above data can be exchanged privately between the parties involved as, unlike Bitcoin protocol, they don't need to be registered on a public medium (e.g. the blockchain).

#### Commitment

Formal timestamped fingerprint expressed as the registration of an hash referring to some structured data over some defined medium expressing time indication and chronological ordering (e.g. the blockchain).

#### Consignment

The data transferred between parties that are subject to client-side validation. There are 2 main types of consignment:

* Contract Consignment: provided by the contract issuer including the main information about the contract
* Transfer Consignment: provided by the payer user party and containing all the state transition history up to the [terminal consignment](#terminal-consignment---consignment-endpoint).

#### Container

The format through which [stash](glossary.md#stash) data are packed and exchanged between users.

#### Contract

A set of [rights](#contract-rights) established and executed digitally between certain parties through RGB protocol. A contract possesses an [active state](../rgb-state-and-operations/state-transitions.md#state-generation-and-active-state) and [business logic](#business-logic), expressed in terms of ownership rights and executive rights. The contract state, rights and conditions of valid operations are defined using RGB [schema](#schema). Only state and operations which allowed by the schema declarations and validation scripts are allowed to happen within the contract scope.

#### Contract Operation

An update to the [contract state](#contract-state) performed according to the rules defined in the contract [schema](#schema).

Contract operations include:

* [State Transition](#state-transition)
* [Genesis](#genesis)
* [State Extension](#state-extension)

#### Contract Participant

An actor which participate in contract operations. Contract parties are classified into the following categories:

* Contract issuer: an actor creating contract [Genesis](#genesis).
* Contract party: all actors which have some [ownership](#ownership) rights over RGB contract state.
* Public party: an actor constructing state extensions. Can exist only in contracts providing valencies and state extensions.

#### Contract Rights

RGB contract parties have a different rights as a part of the contract conditions defined through RGB [Schema](#schema). The rights under RGB contract can be classified into the following categories:

* Ownership rights: the rights associated to the [ownership](#ownership) of some UTXO referenced by a [Seal Definition](#seal-definition).
* Executive rights: the ability to construct the [contract state](#contract-state) in a final form, i.e. to construct a valid [state transition](#state-transition) satisfying [schema](#schema) validation rules.
* Public rights: a right under some schema to use a contract [valency](#valency) and construct a valid [state extension](#state-extension) 

#### Contract State

The set of up to date, private and public information and data related to a contract. In RGB the contract state is constituted by:

* [Global State](rgb-state-and-operations/components-of-a-contract-operation.md#global-state)
* [Owned State](rgb-state-and-operations/components-of-a-contract-operation.md#owned-states)

#### Deterministic Bitcoin Commitment - DBC

The set of rules which allows for the registration of a provably single [commitment](glossary.md#commitment) in a Bitcoin transaction. Specifically, RGB protocol embeds 2 forms of DBC:

* [Opret](../commitment-layer/deterministic-bitcoin-commitments-dbc/opret.md)
* [Tapret](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md)

#### Directed Acyclic Graph - DAG

A directed graph which do not contains any directed cycle thus allowing topological ordering - [wiki link](https://en.wikipedia.org/wiki/Directed\_acyclic\_graph)

#### Engraving

An optional fingerprint that past owners of a contract can register allowing verification of following users. It is implemented in RGB21 interface.

#### Extra Transaction Proof - ETP

The part of the [Anchor](../commitment-layer/anchors.md) which embeds the additional data necessary for the validation of [tapret](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md) commitment contained in a [taproot](#taproot) transaction, such as the internal PubKey and the Script Path Spend.

#### Genesis

The set of data, regulated by a contract [schema](glossary.md#schema), which represent the starting state of every contract of RGB. It's the equivalent of Bitcoin Genesis Block at the client-side level. [Link](../rgb-state-and-operations/state-transitions.md#genesis).

#### Interface

The set of instructions that allows to transform contract binary data of contracts [schema](#schema) and [states](#contract-state)  in user and wallet-readable information.

### Invoice

A Base58 encoded string, which support URL scheme capabilities, embedding the necessary data in order to allow a payer counterpart to construct a [State Transition](#state-transition).

#### Multi Protocol Commitment - MPC

The Merkle Tree structure used in RGB to include in a single commitment into the Bitcoin Blockchain multiple contract state transitions of different contracts.[Link](commitment-layer/multi-protocol-commitments-mpc.md)

#### Ownership

The control and thus the possibility to spend an [UTXO](#utxo) to which some client-side property are [assigned](#assignment).

#### Schema

The set of rules and business logic according to which an RGB contract works.

#### Seal Definition

The reference part of an [Assignment](#assignment) which bind the commitment to an UTXO belonging to the new [owner](#ownership). [Link](../rgb-state-and-operations/components-of-a-contract-operation.md#seal-definition)

#### Shard

A branch of the [DAG](#directed-acyclic-graph---dag) chain of the RGB [state transition](#state-transition).

#### Single-Use Seal

A promise to [commit](#commitment) to a yet unknown message in the future, once and only once, such that commitment fact will be provably known to all members of a certain audience. [Link](../distributed-computing-concepts/single-use-seals.md)

#### Stash

The set of client-side data related to [contract](#contract) over which have undergone [validation](#client-side-validation) and are stored by the users.

#### State Extension

A contract operation which allows for the redeeming of some [Valencies](#valency). It needs to be closed by a [State Transition](#state-transition) in order to put in effect the changes to the contract expressed by the Valencies. [Link](../rgb-state-and-operations/state-transitions.md#state-extensions)

#### State Transition

The most important [contract operation](#contract-operation) which make possible the transition of an RGB State to a New State, changing state data and/or ownership.[Link](../rgb-state-and-operations/state-transitions.md#state-transitions-and-their-mechanics)

#### Taproot

The Segwit v1 transaction format detailed in [BIP341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) and [BIP342](https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki).

#### Terminal Consignment - Consignment Endpoint

The last state of a contract which include the last [State Transition](#state-transition) constructed from a payee counterpart invoice.

#### Transition Bundle

A set of RGB [State Transition](#state-transition), belonging to the same contract, which are constructed by different parties closing their seal in a single operations. [Link](../rgb-state-and-operations/state-transitions.md#transition-bundle)

#### UTXO

A Bitcoin Unspent Transaction Output. It is defined by a transaction hash and and index which, collectively, constitute an [outpoint](https://en.bitcoin.it/wiki/Protocol_documentation#tx).  

#### Valency

A public rights having no state but which can be referenced and redeemed through a state extension.[Link](../rgb-state-and-operations/components-of-a-contract-operation.md#valencies)

#### Witness Transaction

The transaction which provide the [Seal](#single-use-seal) closing operation around a message which contain RGB commitment to a [State Transition](#state-transition)


---