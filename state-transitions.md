# State Transitions



In order to tackle the most characteristic features of RBG Consensus we will be walking through the following steps:
1. Analyze how a **State Transitions** works from the the Client-side perspective and the related *point of contacts* which tether such operation with the Bitcoin Blockchain commitments which were discussed in the [Client-side Validation with Bitcoin](csv-w-btc.md) section.  
2. Study the components of the RGB State in terms of structure and data, and the operation that undergo in state transition operation according to the RGB architecture rules.


## State definition and its evolutions 

First of all, it's important to visualize in simple terms what a *State Transition* actually is. 

Of course, to do that, a definition of [State]() is required, without going into the specific implementation details of RGB which will be covered later. Simply put:

> A State can be defined as a unique configuration of information / data that represents the conditions of a contract in some precise moment in time.

Thus a State Transition, in general terms, represents any **update of data** from an **old state** to a **new state** following the **rules inscribed into the contract** constituting its **Business Logic**. 

![Alt text](img/state-transition-1.png)

The chain of state transitions is the ordered path that make contract data evolve from the very **first contract definition**, called the [**Genesis**]() up to the [**Terminal State**]() representing the most updated state at the tip of the [DAG](terminology/glossary.md#directed-acyclic-graph---dag) of state transitions.

The order relation among the state transitions in maintained thanks to the commitments that anchors the client-side validated data to the Bitcoin Blockchain


## Introduction to State Transition 

The approach followed in this paragraph is the same as the one developed in the [TxO2 Client-side Validation](/csv-w-btc.md#txo2-client-side-validation) using our beloved cryptographic characters Alice and Bob. This time the explanation contains an important difference: this time Bob is not simply validating the client-side validated data that alice shows him. He is effectively asking Alice to add some additional data which **will give Bob some degree of ownership** over the contract expressed as a hidden reference to one of his bitcoin UTxO. Let's see how the process works in practice.

Alice has a [stash]() of client side validated data, which themselves reference to some Bitcoin UTXO owned by her. This means that in her client-side validate data there is a **seal definition** pointing to that UTXO. 

![Alt text](img/stab1.png)

Bob, in turn, possesses some unspent UTXO as well. This UTXO is completely unrelated to Alice's meaning that there is no direct spending event between them. 

<!---
![Alt text](img/stab2a.png)
-->

![Alt text](img/stab2b.png)

Bob, trough some information data, encoded in an **[invoice]()**, instruct Alice to create a **New state** which follows the contract rules and which embed a **new seal definition** which points to the his UTXO in a concealed form. This way Alice is assigning Bob **some ownership** of the new state (e.g. the property of a certain amount of tokens). 

![Alt text](img/stab3.png)

After that, Alice using some [PSBT]() wallet tool, prepares a transaction which spend the UTXO which were pointed by the previous seal definition (the one that passes the ownership to her). This transaction, which is a **witness (seal closing) transaction**,  embeds in his output a commitment to the new state data which uses [Opret](/csv-w-btc.md#opret) or [Tapret](/csv-w-btc.md#tapret) rules depending on the method chosen. As explained previously, the Opret or Tapret commitment derive from a [MPC](/csv-w-btc.md#mpc-tree-construction) tree which can collect more than one contract's state transition. 

Before broadcasting the transaction prepared in this way she passes to Bob a package of data called [consignement]() which contain the stash of client side validated already in possession of alice in addition to the new state.


After checking the correctness of the consignement Bob can give "green light" (for example by means of GPG signing) to Alice to let her broadcast the transaction. When confirmed, the **witness (seal closing) transaction** represent the conclusion of the state transition from Alice to Bob. 


![Alt text](img/stab4.png)


## Anatomy of a State Transition
