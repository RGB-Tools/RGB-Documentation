---
description: Terminology used in RGB sorted in alphabetical order
---

# Glossary

### Anchor

Set of client-side data that proof the inclusion of a unique commitment inside a transaction. In RGB protocol it is constituted by:

* The Bitcoin transaction ID of the [witness transaction](glossary.md).
* The [MPC](glossary.md#multi-protocol-commitment---mpc)
* The [DBC](glossary.md#deterministic-bitcoin-commitment---dbc)
* The [ETP](glossary.md#extra-transaction-proof---etp) in case of [Tapret](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md) commitment scheme.

### AluVM

Acronym of Algoritmic logic unit Virtual machine is register-based virtual machine for smart contract validation and distributed computing, used but not limited to RGB contract validation.

&#x20;[Link](https://www.aluvm.org/)

### Assignment

The RGB-equivalent of a transaction output modifying, updating or creating some properties of the state of a [contract](glossary.md#contract). It is formed by:

* A [Seal Definition](glossary.md#seal-definition)
* An [Owned State](../rgb-state-and-operations/components-of-a-contract-operation.md#owned-states)

[Link](../rgb-state-and-operations/components-of-a-contract-operation.md#assignments-of-an-owned-state)

### Business Logic

The set of operation and rules contained in a contract [Schema](glossary.md#schema) which allows for the rightful update of the [contract state](glossary.md#contract-state).

### Client-side Validation

The operation which allows the verification of some data exchanged between parties according to some defined protocol rules. In RGB protocol these data are in form of [consignment](glossary.md#consignment); the above data can be exchanged privately between the parties involved as, unlike Bitcoin protocol, they don't need to be registered on a public medium (e.g. the blockchain).

### Commitment

It can be seen as the digital equivalent of an envelope containing some text/data whose contents you do not want to reveal right away. It consists of two algorithms: 
- ***commit***: takes a public message, called $msg$, and a random value, called $r$, that will be kept secret until a certain event occurs and returns a value, this value being $com = commit(msg, r)$;
- ***verify***: takes the value returned by the commit algorithm, the public message and the (previously) secret value and returns True/False, $verify(msg, com, r) \rightarrow \text{accept or reject}$.

The commitment algorithm is required to have two security properties: 
- ***binding***: requires that there cannot be two valid "openings" of the same commitment. That is, no adversary can produce $msg'$ and $r'$ such that, given $com$, then $verify(msg,r)=verify(msg',r') \rightarrow True$ and $msg \neq msg'$; 
- ***hiding***: requires that $com$ not let the committed data leak out, i.e., that $r$ be uniformly sampled in a set $R$ such that it is statistically independent of $msg$ (also taken from the set $R$).

In RGB, the so-called [Pedersen commitment](glossary.md#pedersen-commitment) is used for several operations related to [anchors](../commitment-layer/anchors.md).

### Consignment

The data transferred between parties that are subject to [client-side validation](glossary.md#client-side-validation). There are 2 main types of consignment:

* Contract Consignment: provided by the contract issuer including the main information about the contract
* Transfer Consignment: provided by the payer user party and containing all the state transition history up to the [terminal consignment](glossary.md#terminal-consignment---consignment-endpoint).

### Container

The RGB format through which [stash](glossary.md#stash) data are packed and exchanged between users.

### Contract

A set of [rights](glossary.md#contract-rights) established and executed digitally between certain parties through RGB protocol. A contract possesses an [active state](../rgb-state-and-operations/state-transitions.md#state-generation-and-active-state) and [business logic](glossary.md#business-logic), expressed in terms of ownership rights and executive rights. The contract state, rights and conditions of valid operations are defined using RGB [schema](glossary.md#schema). Only state and operations which allowed by the schema declarations and validation scripts are allowed to happen within the contract scope.

### Contract Operation

An update to the [contract state](glossary.md#contract-state) performed according to the rules defined in the contract [schema](glossary.md#schema).

Contract operations include:

* [State Transition](glossary.md#state-transition)
* [Genesis](glossary.md#genesis)
* [State Extension](glossary.md#state-extension)

### Contract Participant

An actor which participate in contract operations. Contract parties are classified into the following categories:

* **Contract issuer**: an actor creating contract [Genesis](glossary.md#genesis).
* **Contract party**: all actors which have some [ownership](glossary.md#ownership) rights over RGB [contract state](glossary.md#contract-state) which have been provided trough an [Assignment](glossary.md#assignment).
* **Public party**: an actor which is able to construct [State Extensions](glossary.md#state-extension). Can exist only in contracts providing [Valencies](glossary.md#valency) to be redeemed by State Extension.&#x20;

### Contract Rights

RGB contract parties have a different rights as a part of the contract conditions defined through RGB [Schema](glossary.md#schema). The rights under RGB contract can be classified into the following categories:

* Ownership rights: the rights associated to the [ownership](glossary.md#ownership) of some UTXO referenced by a [Seal Definition](glossary.md#seal-definition).
* Executive rights: the ability to construct the [contract state](glossary.md#contract-state) in a final form, i.e. to construct a valid [state transition](glossary.md#state-transition) satisfying [schema](glossary.md#schema) validation rules.
* Public rights: a right under some Schema to use a contract [Valency](glossary.md#valency) and construct a valid [State Extension](glossary.md#state-extension).

### Contract State

The set of up to date, private and public information manifesting the condition of a contract at a certain point in history. In RGB the contract state is constituted by:

* [Global State](../rgb-state-and-operations/components-of-a-contract-operation.md#global-state)
* [Owned State(s)](../rgb-state-and-operations/components-of-a-contract-operation.md#owned-states)

### Deterministic Bitcoin Commitment - DBC

The set of rules which allows for the registration of a provably single [commitment](glossary.md#commitment) in a Bitcoin transaction. Specifically, RGB protocol embeds 2 forms of DBC:

* [Opret](../commitment-layer/deterministic-bitcoin-commitments-dbc/opret.md)
* [Tapret](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md)

### Directed Acyclic Graph - DAG

A directed graph which do not contains any directed cycle thus allowing topological ordering. A Blockchain or an RGB Contract [Shard](glossary.md#shard) are examples of DAG.&#x20;

&#x20;[Wikipedia link](https://en.wikipedia.org/wiki/Directed\_acyclic\_graph)

### Engraving

An optional fingerprint that past owners of a contract can register allowing verification of following users. It is implemented in RGB21 [interface](glossary.md#interface).

### Extra Transaction Proof - ETP

The part of the [Anchor](../commitment-layer/anchors.md) which embeds the additional data necessary for the validation of [tapret](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md) commitment contained in a [taproot](glossary.md#taproot) transaction, such as the internal PubKey and the Script Path Spend.

### Genesis

The set of data, regulated by a contract [schema](glossary.md#schema), which represent the starting state of every contract of RGB. It's the equivalent of Bitcoin Genesis Block at the client-side level.

[Link](../rgb-state-and-operations/state-transitions.md#genesis)

### Interface

The set of code instructions that allows to transform the compiled binary data of contracts [Schema](glossary.md#schema) and [Contract Operation](glossary.md#contract-operation) on [States](glossary.md#contract-state) in user and wallet-readable information.

[Link](../rgb-contract-implementation/interface/)

### Interface Implementation

The set of code declarations which bind an [Interface](glossary.md#interface) to a [Schema](glossary.md#schema) and making possible the semantic translation operated by the Interface itself.

### Invoice

A [base58](https://en.wikipedia.org/wiki/Binary-to-text\_encoding#Base58) encoded string, which support URL scheme capabilities, embedding the necessary data in order to allow a payer counterpart to construct a [State Transition](glossary.md#state-transition).

### Multi Protocol Commitment - MPC

The Merkle Tree structure used in RGB to include in a single commitment into the Bitcoin Blockchain multiple [Transition Bundles](glossary.md#transition-bundle) of different contracts.

[Link](commitment-layer/multi-protocol-commitments-mpc.md)

### Ownership

The control and thus the possibility to spend an [UTXO](glossary.md#utxo) to which some client-side property are [assigned](glossary.md#assignment).

### Pedersen commitment

This is a particular type of cryptographic commitment that has the property of being partially homomorphic. This means that given a certain $commit$ function, it is possible to verify the commitment given by the sum of two data without revealing the data itself. That is, given $msg_1$, $msg_2$, $r_1$ and $r_2$, we can verify:

$$com_1 \cdot com_2 = commit(msg_1+msg_2,r_1 + r_2)$$

without revealing the individual summed/multiplied values. This is extremely useful if we want to conceal the amounts of tokens transacted without sacrificing cryptographic security.

### Redeem

A construct present in [State Extension](glossary.md#state-extension) which reference a previously-declared [Valency](glossary.md#valency).

### Schema

A declarative piece of code which contains the set of variables, rules and [business logic](glossary.md#business-logic) according to which an RGB contract works.

[Link](../rgb-contract-implementation/schema/)

### Seal Definition

The reference part of an [Assignment](glossary.md#assignment) which bind the commitment to an UTXO belonging to the new [owner](glossary.md#ownership).&#x20;

[Link](../rgb-state-and-operations/components-of-a-contract-operation.md#seal-definition)

### Shard

A branch of the [DAG](glossary.md#directed-acyclic-graph---dag) chain of the RGB [State Transitions](glossary.md#state-transition).

### Single-Use Seal

A promise to [commit](glossary.md#commitment) to a yet unknown message in the future, once and only once, such that commitment fact will be provably known to all members of a certain audience.

&#x20;[Link](../distributed-computing-concepts/single-use-seals.md)

### Stash

The set of client-side data related to [contract](glossary.md#contract)  which have undergone [validation](glossary.md#client-side-validation) and are stored by the users.

### State Extension

A contract operation which allows for the redeeming of some [Valencies](glossary.md#valency). It needs to be closed by a [State Transition](glossary.md#state-transition) in order to put in effect the changes to the contract expressed by the Valencies.

&#x20;[Link](../rgb-state-and-operations/state-transitions.md#state-extensions)

### State Transition

The most important [contract operation](glossary.md#contract-operation) which make possible the transition of an RGB State to a New State, changing state data and/or ownership.

[Link](../rgb-state-and-operations/state-transitions.md#state-transitions-and-their-mechanics)

### Taproot

The Bitcoin's Segwit v1 transaction format detailed in [BIP341](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) and [BIP342](https://github.com/bitcoin/bips/blob/master/bip-0342.mediawiki).

### Terminal Consignment - Consignment Endpoint

The last state of a contract which include the last [State Transition](glossary.md#state-transition) constructed from a payee counterpart invoice.

### Transition Bundle

A set of RGB [State Transition](glossary.md#state-transition), belonging to the same contract, which are constructed by different parties closing their seal in a single operations.

&#x20;[Link](../rgb-state-and-operations/state-transitions.md#transition-bundle)

### UTXO

A Bitcoin Unspent Transaction Output. It is defined by a transaction hash and and index which, collectively, constitute an [outpoint](https://en.bitcoin.it/wiki/Protocol\_documentation#tx).

### Valency

A public rights having no state but which can be referenced and redeemed through a state extension.

[Link](../rgb-state-and-operations/components-of-a-contract-operation.md#valencies)

### Witness Transaction

The transaction which provide the [Seal](glossary.md#single-use-seal) closing operation around a message which contains the RGB commitment to a [State Transition](glossary.md#state-transition).

***
