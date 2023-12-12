# Technical Introduction

Before going entering into the technical details of the RGB, an introduction over the fundamental elements of the protocol, the environment undepinning the technological substrate, as well as the base terminology represent an essential step towards a thorough understanding of the subject.

## Paradigm of Distributed Computing

* RGB locate itself as a new additional piece of the vast word of *Distributed Computing*.
* Distributed computing, is a branch of Computer Science which study the protocol systems able to exchange and compute data information between of a network of computer nodes: the set of computer nodes and the undelying protocol rules which allows the computation are the contituents of the **Distributed system**.  
  * The nodes, composing the network are able to indipendently verify and validate such set of data and they can contruct, depending on the protocol, complete or partial snapshots of the properties of the network: these are **state** of the distributed system and essentially represent the expression of properties and the underlying agreement over that properties that are established during network operations.
  * The most important properties of a Distributed Systems is represented by the **chronological ordering** of the operations and thus the **ordered sequence of state changes** that take place inside the system. In fact when we talk about **Consensus**, we are talking about:
    1.  **recognized validity of the state transitions** by the nodes and most importantly,
    2.  **consensus on the order of the state transitions** so that every node knows which operation precedes the other.
  * The achievement of a *resilient and reliable* chronological ordering for distributed system, which embed important properties such as permissionlessness and censorship resistance, was reached by Satoshi Nakamoto with the invention of Bitcoin, using the blockchain data structure and a **Proof-of-Work** consensus which is able to entrust differrent participants to the system according to their computational power. Indeed Bitcoin can be considered to be the first working example of **Distributed Consensus System**.     

We will discuss various kind of **Distributed Consensus Systems** which have some degree of hierarchy and interrelated properties between them. They are differentiated on how to dermenine and enforce the most updated state of the system:
* **Blockchain /Timechain + PoW Mechanism (layer 1)**. The sequence of **state transitions** is public and auditable and is organized in **transaction** included in ordered blocks which are added one upon the other. The security of the system lies on the amount of work required to produce an alternative chain which revert the actual greater-work chain which is considered as the valid chain. For instance **Bitcoin** is based on this technological stack.
* **State channels (Layer 2)**. Is a system constructed between 2 (or more) parties and which depend hierarchically on layer 1. The final state is represented by the last transaction out of sequence of ordered invalidating transactions, signed and agreed by the parties *off-chain*. The final state can be enforced by each parties by publishing that last valid transaction on the layer 1. The most developed application of state channels is the **Lightning Network**.
* **Client Side Validated Data -Stash (Layer 3)** Is a system that can be implemented on both blockchain and to state channels and it is based on a certain *limited* amount data whose validity, computation tasks and update is entrusted to each node. Differently form layer 1, the data to be validated by each client node represent a **defined subset of the entirery of all state transitions of the network, and NOT every transition happened within the network**. This validated subset of data in possession of a client node is defined a **Stash** of the data. Basically, the client needs to validate the whole history of the state transitions occurred from the start to the last the transition (a so called **Shard**) and which relate the exchange and the validation of certain digital properties among the counterpary involved. Seen as a whole, the validation mechanism of the shard which produce the stash is called **Client-side Validation** and underpin all **RGB** operations.
 
![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/ac60cc0d-0d3f-4dbd-a7c5-2cef5ac1b765)  
*The 3 set of Distributed System - Blockchain (layer1) is self-sustaining while the other 2 rely on layer 1 for operating - layer 3 can operate on top of both blockchain and state channels*

In order to precisely frame the applications of each Distributed Consensus System and their undelying data structure it's important to understand the limitations that affect each one of these technology. This condition is expressed in form of a **Trilemma** which is connected to an important theoretical result of Distributed Computing, known as **[CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)**. Indeed the therorem states that:

> Any distributed data store can provide only two of the following three guarantees:
> * Consistency - Every read receives the most recent write or an error.
> * Availability - Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
> * Partition tolerance - The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/022ad2c0-f07d-4754-a3e6-a150bd64abdf)  
*Application of CAP Theorem to Distributed Consensus System - Each Distributed Consensus System can fit 2 and only 2 of the properties*

Seen from a more consensus-focussed point of view, the properties of the theorem can be seen also see the 3 properties from this angle: 

* Consistency > Integrity
* Availability > Decentralization
* Parition Tollerance > Scalability and Confidentiality

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/7692116c-f13b-4a06-bb39-d649a0dce10c)  
*A more in-depth view of th inherent degree of application of the Trilemma to Distributed Consensus System*  
In syntesis:

* Blockchain (layer 1) preserve Integrity and Decentralization but lacks Scalability and Confidentiality as each node need to replicate *publicly and in-full* every state transition
* State Channels (layer 2) preserve Decentralization and Scalability but doesn't preserve the Integrity as the state can be changed or updated asyncrnously by the counterparties.
* Client Side validated data (layer 3) are Scalable and maintin Integrity, however some data are not decentralized and hence lack Availability. Thus a single point of centralization of the data (e.g. the issuer) is required.  

An important feature to take into account is the different way through which State Channel and Client-Side validation architectures update the state of the data:

* State Channel state must be **syncronous** with the counterpary
* Client side validated state update can be **asyncronous**

Naturally, if the client-side validated data are embedded in state channels, the update of the state will follow an asyncronous process. 
In the next section we will delve into Client-side Validation and its features.  


## Client-side Validation

 The goal of every validation process od a distributed system machine is the ability to assess the validity and the chronological ordering of the states, hence to map the state transitions that took place.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/463eea67-d5e9-401c-916e-bce7357a538e)

 In Bitcoin Blockchain, for instance, such process maps the change in the [UTXO](https://en.wikipedia.org/wiki/Unspent_transaction_output) determined by the transactions collected into the sequence of ordered blocks. Every block represent a state update.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/1d209128-de76-40ab-b291-373b1c74440a)

The main drawback of Layer 1 validation process is that **every node needs to validate each transaction from everybody** and store the related data and this architecture lead to two main issues:
* Scalability: the size limit of the blocks vs. the demand of blockspace per unit time shared by all the participants willing to transact (i.e. 1 MB on ~10 minutes on average on bitcoin)   
* Privacy: the detail of each transactions are broadcasted and stored in public form ( in particular: the amounts transacted and the receiving adressess, albeit pseudonimous)
  
![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/403da928-31a8-4e08-8707-9c1f853df067)

However, from the point of a transaction recipient the only aspectes that matters are:
* the last state of a specific property that will change through a transaction addrressed to him and,
* the chronological sequence of transactions (and thus state transitions) that lead to the that last state.s

Basically what is important to him is the [Directed Acyclic Graph](#) which connect the history of state transitions to the last state addressed to him (a **Shard** of the whole data)

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/6f81258f-1326-46e8-a951-16bc61163784)


For this reason, the **logic of validation can be resersed** in the following terms:
* Each party validates **its own part of the history** and thus the digital properties that matters to him
* A compact reference to the **validated state transition is committed to the first layer**  which constitue a **Proof-of-Pubblication** and an anti-double-spend measure. 

These are the principles behind **Client-side Validation**

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/3c241331-abfa-42d9-af48-2d9bcb1aad33)

This ensures the respect of:
* Scalability: as the commitment of the verified state, which need to be stored by everyone, has a small size footprint (order on tens of byte)
* Privacy: by using a hash one-way function (such as SHA-256), the original data (the pre-image) reference by the commitment cannot be inferred, and, in addition, are kept private by the parties.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f429b7b9-2ddc-4701-94f0-296ce8144be0)

The commitment structure used in client side validations (such as in RGB protoco which we will cover in depth later) allows important additional scalability. Indeed each possessor with a single commitment can: 

* aggregate the state transitions of different properties (for example two different contracts pertaining to 2 different digital assets)
* bundle more than one state transition of the same asset   

In order to guarentee the efficacy of the commitment scheme and a precise chronologica ordering stemmed from the layer 1, the use of a new cryptographic primitive needs to be introduced: the **Single-use Seal**.

## Single-use Seals

A Single-use seal is a form of **cryptographical commitment** which resemble the application of a physical seal to a box containing some objects, which allows to prove a sequence of events limiting the risk that this sequence of events can be altered after being set. This implies that such commitment scheme, [proposed](https://petertodd.org/2016/commitments-and-single-use-seals) by Peter Todd in ~2016, is more advanced than `simple commitments` and `timestamping`.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/984ef35b-6410-4eac-8163-d08b0ccc049e)

In order to work properly, Single-use seals require:

* a **Proof of Pubblication Medium**  - This can be a medium with global consensus (like layer 1 blockchain) but not necessarily decentralized, for example a newspape, which has the ability to be difficult to alterated once issued and made public.
* to prove that a certain message `m` has been received by *every* member of a certain audience
* to prove, conversely, that a certain message `m` has not (yet) published
* to prove that no other alternative medium has not been used to publish the message

With this properties we can state a formal definition:

> A single-use Seal is a commitment formal promise to commit to a (yet) unknown message in the future, once and only once, such that commitment fact will be provably known to all members of a certain audience.

With such definition and the general properties reported above, a single use seal can achieve simultaneously the following 3 properties:

 * the pubblication of the commitment doesn't reveal the original message (e.g. using a one-way hash function)  - this property is also shared by simple commitment and timestamps
 * it proofs the commitment time and the fact that the original message existed before a certain date - this property is shared by timestamps only
 * it proofs that no alternative valid commitment can exists - this property is unique of single use seals

So, how we can contruct practically a Single-use Seal? And what can be used? In a general way, it's working principles comprises 3 steps:

* Seal Definition
* Seal Closing
* Seal Verification

For the sake of the examples we will be using the well known cryprographic characters Alice and Bob.

**Seal Defintion** 
 
In Seal definition, Alice promise to Bob (either in private or in public) to create a **commitment** to some **message**:

* at a well definied point in time and space 
* using a precise medium of information

**Seal Closing**

When Alice publish the **commitment** following all the features stated in the **definition**, in addition she produces a **witness** which is the proof that the seal has been actually closed.  

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/3711069c-af89-494f-be31-dfeaa960d841)


**Seal Verification**
      
Once closed, the seal, being "single-use", cannot be opened nor closed again. The only thing that can be done (by Alice) is to verify if the seal has been actually closed around the commitment of the message, by using the seal, the witness and the commitment (to the message).

In Computer Science Language the whole procedure can be summed-up as follows:
```
Define() -> seal  (done by Alice, accepted by Bob)

Close(seal, commitmet(message)) -> witness    (close a seal over a message, done by Alice

Verify(seal, witness, commitment(message)) ->  true|false  (verify that the seal was closed, done by Bob)
```

So making a recap:

* With single-use-seal you can build client-side-validated systems which does not require global consensus (“blockchain”) storing all of the data.
 * This gives scalability and  privacy
 * Single-use-seal definition made on the client side, not necessary in the global consensus medium
* However, **you can’t prove the definition of the seal itself** even if you a member of audience observing the pubblication medium

 `Thus we need a “chain” of single-use-seals, where **the commitment to the message of previous seal defines the next seal(s): this is what RGB does together with Bitcoin**:
 * the messages are client-side validated data
 * the seal definitions are bitcoin UTXO
 * the commitment is an hash placed inside bitcoin transaction
 * the seal closing can be either an UTXO being spent or an addressed to which a transaction credit some bitcoins 
 
 Now we will explore in details how RGB implements the single use seal concept, storing commitment to its operation in the bitcoin blockchain.





