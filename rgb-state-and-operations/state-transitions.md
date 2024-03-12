# Contract Operations

## State Transitions and their mechanics

The approach followed in this paragraph is the same as that developed in the [TxO2 Client-side Validation chapter](../commitment-layer/commitment-schemes.md#txo2-client-side-validation) using our beloved cryptographic characters Alice and Bob.&#x20;

This time the explanation **contains an important difference**: Bob is not simply validating the client-side validated data that Alice shows him. He is actually asking Alice to add some additional data that **will give Bob some degree of ownership** over the contract expressed as a hidden reference to one of his Bitcoin [UTXOs](../annexes/glossary.md#utxo). Let's see how the process works in practice for a [State Transition](../annexes/glossary.md#state-transition) (one of fundamental [Contract Operations](../annexes/glossary.md#contract-operation)):

1. Alice has a [stash](../annexes/glossary.md#stash) of client-side validated data, which in turn reference a Bitcoin UTXO owned by her. This means that in her client-side validate data there is a [seal definition](../annexes/glossary.md#seal-definition) that points to one of her UTXOs.

<figure><img src="../.gitbook/assets/stab1.png" alt=""><figcaption><p>At the beginning of the State Transition, Alice possesses a certain stash and a UTXO. The idea behind the operation is that she will pass some digital rights in her possession to Bob.</p></figcaption></figure>

2. Bob, in turn, also has unspent UTXOs. These UTXOs are completely unrelated to Alice's, which means that there is no direct spending event that creates a link between them.

<figure><img src="../.gitbook/assets/stab2b.png" alt=""><figcaption><p><strong>Bob also owns some UTXOs. Moreover, they are unrelated to Alice's. This UTXO is a fundamental requirement to complete the State Transition.</strong></p></figcaption></figure>

3. Bob, through some informational data, encoded in an [invoice](../annexes/glossary.md#invoice), instructs Alice to create a **New state** that follows the rules of the contract and which embeds a **new seal definition** pointing to one his UTXOs in a concealed form (more on that later). In this way, Alice assigns Bob **some ownership** of the new state: for example, ownership of a certain amount of tokens.

<figure><img src="../.gitbook/assets/stab3.png" alt=""><figcaption><p><strong>Bob, cooperates with Alice in the State Transition by providing the data necessary for Alice to build the new state.</strong></p></figcaption></figure>

4. After that, Alice, using some [PSBT](../annexes/glossary.md#partially-signed-bitcoin-transaction-psbt) wallet tool, prepares a transaction which spends the UTXOs that were indicated by the previous seal definition (the very same one that granted her ownership of some elements of the contracts). In this transaction, which is a [witness transaction](../annexes/glossary.md#witness-transaction), Alice embeds in one output a commitment to the new state data that uses [Opret](../commitment-layer/deterministic-bitcoin-commitments-dbc/opret.md) or [Tapret](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md) rules depending on the method chosen. As explained earlier, Opret or Tapret commitments are derived from an [MPC](../annexes/glossary.md#multi-protocol-commitment-mpc) tree which can collect more than one contract's state transition.
5. Before transmitting the transaction thus prepared, Alice passes to Bob a data packet called [Consignment](state-transitions.md) which contains the organized stash of client-side data already in possession of Alice in addition to the new state. Bob, at this point, through the tools coded in [RGB-core library](../annexes/rgb-library-map.md#rgb-core) and [client-side validation library](../annexes/rgb-library-map.md#client-side-validation):
   * **Validates every RGB state data contained in the RGB Consignment**, including the last New State which assign ownership right to Bob over the contract.
   * Through the Anchors contained in the consignment as well, he **verifies the chronological ordering of the** sequence of [witness transactions](../annexes/glossary.md#witness-transaction) which took place from Genesis to the last state and the related commitments pointing at RGB data contained herein.
6. After checking the correctness of the Consignment, Bob can give Alice a "go-ahead" signal (e.g., by GPG signature) and allows her to broadcast this last witness transaction, containing the New State. Once confirmed, such witness transaction represents the conclusion of the [State Transition](../annexes/glossary.md#state-transition) from Alice to Bob.

<figure><img src="../.gitbook/assets/stab4.png" alt=""><figcaption><p>T<strong>he new state points to Bob's UTXO by assigning him the digital property once in Alice's possession. The new state is committed in the witness transaction that spends the UTXO, which in turn proves Alice's ownership over the digital property that is passed over to Bob. The spending of the UTXO by Alice marks the completion of the State Transition embedding the same level of anti-dual-spending security as in Bitcoin.</strong></p></figcaption></figure>

It's useful to see the full details of a DAG of two RGB contract operations - ([Genesis](../annexes/glossary.md#genesis) + a State Transition) - both from the RGB client-side components, which will be covered in the next few paragraphs, and from the _connection points_ to the Bitcoin Blockchain which embeds the seal definition and the witness transaction.

![A representation of RGB Laver (red) and  Bitcoin Commitment Layer (orange) and their respective connections during contract operations. The diagram shows the combination of two contract operations: a Genesis, constructing a Seal Definition, and a State Transition which closes the seal previously defined in the Genesis and defines a new seal (new ownership) within another Bitcoin UTXO.  The State Transition bundle is meant to collect more than one State Transition in case multiple seal are closed in the same witness transaction.](../.gitbook/assets/state-transition-2-detail.png)

Just to give an introduction to the context of the above diagram, let us introduce terminology that will be discussed [later](components-of-a-contract-operation.md) in greater technical detail:

* The [Assignment](../annexes/glossary.md#assignment) construct, which is pointed at Alice (in this example by the Genesis), and later used by Alice and pointed at Bob's, is responsible for two things:
  * The [Seal Definition](../annexes/glossary.md#seal-definition) which points to a specific UTXO (to Alice's first, by the Genesis created by a contract issuer, an later to Bob's by Alice herself).
  * The association of the Seal Definition to specific sets of data called [Owned States](../annexes/glossary.md#owned-state) which, depending on the properties of the contract, can be chosen from several types. To give a simple context example, the amount of tokens transferred is a common kind of Owned State.
* [Global State](../annexes/glossary.md#global-state), on the other hand, reflect general and **public properties** of a contract that maintain consistency in the evolution and state changes of the contract.

As mentioned [earlier](intro-smart-contract-states.md#introduction-to-states), a State Transition represents the main form among [Contract Operations](../annexes/glossary.md#contract-operation) (in addition to [Genesis](../annexes/glossary.md#genesis) and [State Extensions](../annexes/glossary.md#state-extension)). The **State Transitions** refer to one or more previously defined state(s) - in genesis or another State Transition - and update them to a **New State**. As an interesting scalability feature of RGB, multiple **State Transitions** can be aggregated in a **Transaction Bundle**, so that **each bundling operation** fits one and only one contract leaf in the [MPC](../annexes/glossary.md#multi-protocol-commitment-mpc) tree.

![A detailed view of a State Transition bundle, where two seal belonging to the same contract are closed by the same witness transaction. The diagram separates the RGB specific part from the Bitcoin Commitment Layer part, referencing the related libraries. ](../.gitbook/assets/state-transition-3-bitcoin-rgb.png)

Following the diagram above:

* All the data participating in the State Transitions, aggregated and hashed, enters contract-wise their respective [Transition Bundle](state-transitions.md#transition-bundle).
* The Transaction Bundle is hashed and committed to the [MPC](../annexes/glossary.md#multi-protocol-commitment-mpc) Tree contract leaf as a [BundleId](state-transitions.md#bundleid).
* &#x20;Thanks to [DBC](../commitment-layer/commitment-schemes.md#deterministic-bitcoin-commitment---dbc) the MPC Tree is committed to a Tapret or Opret output that, at the same time, the underlying message is incorporated in the witness transaction closing the previously defined seals, pointing at their respective Bitcoin UTXOs. Inside the same State Transition some new Seal Definitions are defined through the new assignment together with their related Owned States.&#x20;
* The [Anchor](../commitment-layer/commitment-schemes.md#anchors) represents the _connection point_ between the commitment inside Bitcoin Blockchain and the RGB client-side validation structure.

In the following paragraphs we will delve into all the elements and the process involved in the the State Transition operation. All topics discussed from now on belong to RGB Consensus, which is encoded in the [RGB Core Library](../annexes/rgb-library-map.md#rgb-core).

## Transition Bundle

As an important general feature of RGB protocol, it is possible to bundle **different State Transitions belonging to the same contract** (i.e. having the same `ContractId` which is nothing more than an elaboration of the [OpId](components-of-a-contract-operation.md#opid) of the Genesis operation). **In simplest cases, such as the one shown above between Alice and Bob, a Transition Bundle consists of a single state transition**.

However, RGB embeds into its design support for _Multi-payer operations_ such as Coinjoins and Lightning Channel openings, where multiple paying parties (in addition to Alice) own the same asset. With Transition Bundles, each party can decide to asynchronously and privately construct a State Transaction that transfers ownership of the contract to one (i.e. Bob) or many counterparties (in a _many-to-many_ relationship). Then the parties involved may decide to group these State transitions into Transition Bundle and, following RGB rules for MPC and DBC, constructs a single [witness transaction](../annexes/glossary.md#witness-transaction) which closes all the [seal definitions](../annexes/glossary.md#seal-definition) referenced by the State Transitions inside the Bundle.

### BundleId

From a more technical angle, the `BundleId` to be inserted in the leaf of the [MPC](state-transitions.md), is [obtained](https://github.com/RGB-WG/rgb-core/blob/vesper/doc/Commitments.md#bundle-id) from a tagged hash of the strict serialization of the `InputMap` field of the bundle in the following way:

`BundleId = SHA-256(SHA-256(bundle_tag) || SHA-256(bundle_tag) || InputMap)`

Where:

* `bundle_tag = urn:lnp-bp:rgb:bundle#2024-02-03`

An `InputMap` associated to the i-th `input_i` in the set `i = {0,1,..,N-1}` that references the j-th `OpId` in the set `j = {0,1,..,K}` is a construct built as follows:

```
InputMap = 

         N               input_0    OpId(input_0)    input_1    OpId(input_1)   ...    input_N-1  OpId(input_N-1)    
|____________________| |_________||______________| |_________||______________|       |__________||_______________|
 16-bit Little Endian   32-bit LE   32-byte hash                                         
                       |_________________________| |_________________________|  ...  |___________________________|
                               MapElement1                MapElement2                       MapElementN 
```

where:

* `N` in the total number of inputs of the **witness transaction** that refer to an `OPId(input_i)` in the set `{0,1,...,i}`.
* `OpId(input_j)` is the Operation Identifier of the j-th State Transition included in the Transaction Bundle associated with _i-th_ input of the witness transaction. It is important to remember that each State Transition can have more than one input so that `K <= N`.

**By referring to each input only once in an orderly manner, the possibility to double-spend the same seal definition in two different state transitions is effectively prevented.**

## State Generation and Active State

The important topic of state transitions, just covered in the previous sections, allows the transfer of ownership of certain state properties from one party to another. However, state transitions are not the only type of operation possible in RGB protocol, since they are an element of the larger set of [Contract Operations](../annexes/glossary.md#contract-operation). In particular, in RGB, we have at our disposal three types of contract operations, indicated in the `OpType` construct enclosed within them:

* **State Transition**
* **Genesis**
* **State Extension**

The last two can be referred to as **State Generation** operations, and in the following paragraphs we will explore their properties.

The following figure shows all three contract operations along with their position in a DAG related to an RGB contract, sorted by their respective anchors in the Bitcoin Blockchain: Genesis is in <mark style="color:green;">green</mark>, State Transitions are in <mark style="color:red;">red</mark>, State Extensions are in <mark style="color:blue;">blue</mark>.

<figure><img src="../.gitbook/assets/image (5).png" alt=""><figcaption><p><strong>A DAG related to an RGB contract and the different contract operations. In orange the blocks of Bitcoin's Blockchain in which the commitments are stored and linked to client-side data via anchors.</strong></p></figcaption></figure>

It is important to note that the main difference between ordinary State Transitions and the two State Generation Operations lies **in the lack of the closing part of the seal**. For this reason, **both Genesis and State Extensions require a State Transition that closes the particular seal definition constructed by them**.

Another obvious, but crucial, aspect to keep in mind is that the **Active State(s)** are the last state(s) at the end of the [DAG](state-transitions.md) of contract operations that reference themselves in the order committed into the Bitcoin Blockchain, starting from the Genesis. All other states associated with spent UTXOs are no longer valid but are critical to the validation process.

### Genesis

Genesis represents the **initial data block of each RGB contract.** It is constructed by a [contract issuer](../annexes/glossary.md#contract-participant) and any state transitions or state extensions must eventually be connected to it through the DAG of the contract operations.\
In Genesis, according to the rules defined in the [Schema](../annexes/glossary.md#schema), are defined several properties affecting deeply the contract states, both of [owned](../annexes/glossary.md#owned-state) and [global](../annexes/glossary.md#global-state) form.

To give an example, in the case of a contract defining the creation of a token, the following data are likely to be inscribed in Genesis:

* The number of tokens issued and their owner (the owner of the UTXO referred to in the seal definition's genesis).
* The maximum number of tokens to be issued in total.
* The possibility of re-issuance and the designed party that possesses this right.

As a natural implication, **Genesis does not refer to any previous state transition**, nor does it close any previously defined seal. As mentioned above, to be effectively validated in the history of the chain, a Genesis must be referenced by a first state transition (e.g. an auto-spend to the issuer or a first round of distribution), which finalizes the "first ownership" of the contract through a commitment to the Bitcoin Blockchain.

### State Extensions

This type of operation represents a **new feature** in the smart contract realm. With State Extensions, **some digital right defined in the contract can be redeemed by some specifically defined parties or by the occurrence of some precise events**. This contract operation is used to confer some complex rights to other parties than the contract issuer (who is the Genesis creator) such as those related to:

* _Distributed issuance_ of some token.
* _Token swap_.
* _Re-issuance events_ that may involve bitcoin / other assets _burning_ to some specific address(es).

In the RGB taxonomy, the digital right that is redeemed in a State Extensions is called a [Valency](../annexes/glossary.md#valency), and, at the client-side level, is treated as an assignment that is referenced in an RGB input. In this case, this particular piece of "input" is called [Redeem](components-of-a-contract-operation.md#redeems). Like Genesis, the **State Extensions do not close any seals,** instead, **they define a new seal**. They redeem Valencies defined in Genesis or State Transitions and, in turn, must be closed by a subsequent State Transition.

<figure><img src="../.gitbook/assets/image (6).png" alt=""><figcaption><p><strong>Mechanism of operation of State Extensions. In this example, the State Extension redeems some Valencies from the Genesis and defines a new single-use seal that will then be closed by a subsequent State Transition.</strong></p></figcaption></figure>

Following the figure above, we have an example of the mechanism of operation of state extension in practice:

* As a first step, the contract issuer defines some kind of valency (e.g., an issuance right) in Genesis. For example, the valency may grant a secondary issuance of the token defined in the contact, only if authorized by a valid signature related to a specific public key embedded in the valency.
* A entitled party constructs a state extension that references this valency in the [redeem](../annexes/glossary.md#redeem) part of the transaction. At the same time, an entitlement along with a seal definition pointing to a UTXO is constructed as an assignment in the same state extension. Following the example, the state extension will include a signature matching the signature defined in the valency and assign the new amount of tokens issued to a Bitcoin UTXO as the seal definition.
* The seal definition specified in the state extension is closed through a State Transition constructed by the owner of the UTXO to which the seal definition pointed at. In this way, the state owner is able to spend the newly issued tokens on itself or other parties.

***
