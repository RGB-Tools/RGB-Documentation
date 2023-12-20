---
description: Terminology used in RGB sorted in alphabetical order
---

# GLOSSARY OF TERMS

#### Anchor

Most upper-level commitment of a [client-side-validation](#client-side-validation) scheme inside a transaction. In RGB protocol is constituted by the root hash of a [Multi Protocol Commitment](#) and by a tapret proof (if used in the commitment scheme). 

#### Assignement

The RGB-equivalent of a transaction output modifying the state of a contract.

#### Bundle

A set of RGB assignements[#assignemen] whose state transitions are grouped together at client-side level as they reference to the same contract schema (e.g. asset). 


#### Client-side Validation

The operation which allows the verification of some data exchanged between parties according to some defined protocolo rule. In RGB protocol these data are in form of [consignements](#consignment); the above data can be exchanged privately between the parties involved as, unlike Bitcoin protocol, they dont't need to be registered on a public medium (e.g. the blockchain).

#### Commitment

Formal timestamped fingerprint expressed as the registration of an hash referring to some structured data over some defined medium (e.g. the blockchain)


#### Consignment
The data trasnfered between parties that are subject to client-side validation. There are 2 main types of consignemen:
* Contract Consignment: provided by the contract issues including the main information about the contract
* Transfer Consignment: provided by the payer user party and containing all the state transition hystory up to the [terminal consignment]()

#### Container

The way how stash data are exchanged between users.

#### Contract

A set of rights established and executed digitally between certain parties. A contract has state and business logic, expressed in terms of ownership rights and executive rights. The contract state, rights and conditions of valid operations are defined using RGB schema; only state and operations which allowed by the schema declarations and valdiation scripts are allowed to happen withint the contract scope.

#### Contract State

The set of up to date, private and public information related to a contract. In RGB the contract state is constituted by:
* Global State - public informations
* Owned State


#### Contract Participant

An actor which participate in contract operations. Contract parties are classified into the following categories:

* Contract issuer: an actor creating contract genesis
* Contract party: all actors which has ownership rights over RGB contract state
* Public party: an actor constructing state extensions. Can exist only in contracts providing valencies and state extensions.

#### Deterministic Bitcoin Commitments - DBC

The set of rules which allows for the registration of a provably single [commitment](#commitment) in a Bitcoin transaction. Specifically, RGB protocol embedds 2 forms of DBC:
* Opret
* Tapret

#### Directed Acyclic Graph - DAG

A directed graph which do not contains any directed cycle thus allowing topological ordering - [wiki link](https://en.wikipedia.org/wiki/Directed\_acyclic\_graph)

#### Engraving

An optional fingerprint that past owners of a contract can register allowing verification of following users. It is implemented in RGB21 interface

#### Extra Transaction Proof - ETP

#### Genesis

The set of data, regulated by a contract [schema](), which represent the starting point of every contract of RGB. It's equivalent of Bitcoin Genesis Block in the Client-side Validation domain. 

#### Global State

#### Interface

The set of human and wallet-readable information of an RGB [contract](#contract)

### Invoice

A Base58 encoded string, which supporta URL scheme capabilities, embedding the necessary data in order to allow a payer counterparty to construct a state transition.

#### Multi Protocol Commitment - MPC

The Merkle Tree structure used in RGB to include in a single commitment into the Bitcoin Blockchain multiple contract state transitions of different contracts.

#### Schema

The set of rules and business logic according to which an RGB contract works.

#### Seal Definition

#### Shard

A branch of the DAG of the RGB constract transitions

#### Single-Use Seal

A promise to [commit](#commitment) to a yet unknown message in the future, once and only once, such that commitment fact will be provably known to all members of a certain audience.

#### Stash

The set of client-side data over which have undergone [validation](glossary-of-terms.md#client-side-validation) and are stored by the user.

#### State Extension

#### State Transition

#### Taproot

#### Terminal Consignement - Consignement Endpoint

The final state of a contract which include the last state transition constructed from a payee counterparty invoice.


#### Valency;

A public rights having no state but which can be referenced and  applied through a state extension.
