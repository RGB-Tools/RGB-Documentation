---
description: Terminology used in RGB sorted in alphabetical order
---

# GLOSSARY OF TERMS

#### Anchor

Most upper-level commitment of a [client-side-validation](#client-side-validation) scheme inside a transaction. In RGB protocol is constituted by the root hash of a [Multi Protocol Commitment](#) and by a tapret proof (if used in the commitment scheme).   

#### Client-side Validation

The operation which allows the verification of some data exchanged between parties according to some defined protocolo rule. In RGB protocol these data are in form of [consignement](#consignment); the above data can be exchanged privately between the parties involved as, unlike Bitcoin protocol, they dont't need to be registered on a public medium (e.g. the blockchain).

#### Single -Use Seal

A promise to [commit](glossary-of-terms.md#commitment) to a yet unknown message in the future, once and only once, such that commitment fact will be provably known to all members of a certain audience.

#### Schema

The set of rules according to which an RGB contract works

#### Merkle Tree

#### Stash

The set of client-side data over which have undergone a [validation](glossary-of-terms.md#client-side-validation) operation and are stored by the user.

#### Shard

A branch of the DAG

#### Multi Protocol Commitment - MPC

#### Commitment

Formal timestamped fingerprint expressed as the registration of an hash referring to some structured data over some defined medium (e.g. the blockchain)

#### Commitment Schemes

#### Witness Transaction

#### Seal Definition

#### Public Key

#### Private Key

#### Deterministic Bitcoin Commitment - DBC

#### Extra Transaction Proof - ETP

#### Contract ID

#### Bundle ID

#### Assignment
The RGB equivalent of 

#### Consignment
The data trasnfered between parties that are subject to client-side validation. There are 2 main types of consignemen:
* Contract Consignment: provided by the contract issues including the main information about the contract
* Transfer Consignment: provided by the payer user party and containing all the state transition hystory up to the [terminal consignment]()

#### Global State

#### Contract State

#### Operation ID



#### Contract participant

An actor which participate in contract operations. Contract parties are classified into the following categories:

* Contract issuer: an actor creating contract genesis
* Contract party: all actors which has ownership rights over RGB contract state
* Public party: an actor constructing state extensions. Can exist only in contracts providing valencies and state extensions.


#### Contract Genesis


#### Terminal Consignement - Consignement endpoint

The final state of a contract which include the last state transition constructed from a payee counterparty invoice.

### Invoice

A Base58 encoded string, which supporta URL scheme capabilities, embedding the necessary data in order to allow a payer counterparty to construct a state transition.


#### State Transition

#### State Extension

#### Taproot

#### RGB Contract

A set of rights established and executed digitally between certain parties. A contract has state and business logic, expressed in terms of ownership rights and executive rights. The contract state, rights and conditions of valid operations are defined using RGB schema; only state and operations which allowed by the schema declarations and valdiation scripts are allowed to happen withint the contract scope.

#### Valency;

A public rights having no state but which can be referenced and  applied through a state extension

#### Directed Acyclic Graph - DAG

A directed graph which do not contains any directed cycle thus allowing topological ordering - [wiki link](https://en.wikipedia.org/wiki/Directed\_acyclic\_graph)

#### Interface

The set of human and wallet-readable information of an RGB [contract](#contract)

#### Container&#x20;

The way how stash data are exchanged between users&#x20;

#### Engraving

An optional fingerprint that past owners of a contract can register allowing verification of following users. It is implemented in RGB21 interface

####











