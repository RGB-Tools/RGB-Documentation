# Introduction to Smart Contracts and their States

Before addressing the technical implementation of **RGB states** and the related data structure, it is important to remember that the **ordered sequence of seal definition and subsequent seal closure** is intended to provide the ability to properly implement the various **Contract Operations** in the client-side validated domain.

\
After a brief introduction to **smart contracts** and **state concepts**, we will devote our attention to the mechanism behind **Contract Operations** from the the Client-side perspective and the related bridging _points which_ tether these operations to the Bitcoin Blockchain commitments discussed in the [commitment layer section](../commitment-layer/commitment-schemes.md).

## Smart Contracts and Digital Bearer Rights

Since RGB allows for the implementation of **smart contracts** in Bitcoin, it is a good time to give a definition of what a smart contract actually is.

> A **smart contract** is an agreement which is automatically and computationally enforced between the parties.

This means that the enforcement of the terms agreed upon between the parties **does not require human intervention** and that such enforcement is carried out by mathematical and computerized means.

Furthermore, a question arises. To achieve the highest degree of automation, decentralization, and privacy, is it possible to forfeit the use of a centralized registry that stores ownership and contract information? The affirmative answer lie back at the origins.

![RGB enables digital version of bearer instruments.](../.gitbook/assets/orenoque-contract.png)

Not long times ago, contracts, such as securities, were **bearer instruments**. Indeed, the widespread use of asset registers that in fact imply a custodial relationship with some institution on behalf of the client is a fairly recent development in economic history. **The bearer nature of contracts is in fact a centuries-old tradition.** This type of philosophy is the basis of the RGB architecture, in that **the bearer** rights of each claimant **are contained in the form of data within the contract** and can be modified and applied digitally, following the rules of the contract itself.

## Introduction to States

A wider range of smart contract programmability issues were considered in the design of RGB, in particular:

1. **A contract can be associated with a digital asset or a \_token**\_**, but it's not limited to it**. A broader range of applications and extensions of the _smart contract_ concept can be implemented in RGB.
2. Unlike the approach of other public blockchains to smart contracts, in **RGB there is a clear separation between the different** [parties](../annexes/glossary.md#contract-participant) **related to a contract and the their rights**: e.g. the creator/issuer of the contract and the different kind of users interacting in some ways with the contract. This includes in particular the differentiation between:
   * the ability to _observe_ certain properties or operations performed by other parties on the contract;
   * the ability to _execute a set of operations_ permitted by the contract.

**No other counterparty can interact** with the operations performed on the contract unless it is authorized by the authorized parties. Within RGB this feature means that there is always an [owner](../annexes/glossary.md#ownership) that is a party that owns the right to perform certain operations on the contract, which are defined by the contract itself.

These properties combined allow for two of the most important properties at the heart of the RGB value proposition, which are: **scalability** and **censorship resistance** at unprecedented levels.

In order to achieve this goals, a RGB contract is composed by two main components:

* **State**
* **Business Logic (Behavior)**

In fact, the [Business Logic](../annexes/glossary.md#business-logic) of the contract represents the rules that allow the entitled party (the owner) to change the state of the contract. We will find out later that the **Business Logic** is embedded in a particular structure of the contract called the [Schema](../annexes/glossary.md#schema).

![In order to evolve, smart contract states must fallow a business logic.](../.gitbook/assets/state-business-logic.png)

Without going into the specific details of RGB implementation, which will be covered [later](state-transitions.md), an initial and fundamental definition of [State](../annexes/glossary.md#contract-state) is required. Simply put:

> A **State** can be defined as a unique configuration of information / data that represents the conditions of a contract at a specific point in time.

Therefore, a [Contract Operation](../annexes/glossary.md#contract-operation), in general terms, represents any **first creation / update of data** from an **old state** to a **new state** following the **rules inscribed into the contract** constituting its **Business Logic**.

<figure><img src="../.gitbook/assets/image (4) (1) (1).png" alt=""><figcaption><p><strong>State Transitions (among Contract Operations) apply business logic to an Old state to derive a New state.</strong></p></figcaption></figure>

The chain of Contract Operations in RGB is the ordered path that evolves the contract data from the **first contract definition**, called [Genesis](../annexes/glossary.md#genesis) to the [Terminal State](../annexes/glossary.md#terminal-consignment-consignment-endpoint) that represent the most up-to-date state at the end of the [DAG](../annexes/glossary.md#directed-acyclic-graph---dag) of Contract Operations.

The ordering relationship between the DAGs is maintained through the commitments that anchor the client-side validated data to the Bitcoin Blockchain which, in turn, provides timestamping capabilities and **source of ordering**.

***
