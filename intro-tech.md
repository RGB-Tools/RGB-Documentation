# Technical Introduction and Base Concepts

Before divining into the technical details of the RGB, the introduction to the fundamental concepts of the technology, as well as the study of the base terminology represent the essential step towards a thorough understanding of the subject.

## Paradigm of Distributed Computing

* RGB locate itself as a new additional piece of the vast word of *Distributed Computing*.
* Distributed computing, is a branch of Computer Science which study the protocol systems able to exchange and compute data information between of a network of computer nodes: the set of computer nodes and the undelying protocol rules which allows the computation of these data are the contituents of **Distributed systems**.  
  * The nodes, composing the network are able to indipendently verify and validate some set of data and they can contruct, depending on the protocol, complete or partial snapshots of the set of information elaborated by the network: these are called the **states** of the distributed system and essentially represent the expression of properties and the underlying agreement over those properties that are established during network operations.
  * The most important properties of a Distributed Systems is represented by the **chronological ordering** of the operations and the data and thus the **ordered sequence of state changes** that take place inside the system. In fact when we talk about **Consensus**, we are talking about:
    1.  **recognizing the validity of the state transitions** by the nodes according to the protocol rules.
    2.  **establishing consensus on the order of the state transitions** so that every node knows which operation precedes the other and the state cannot be reversed once it has changed: the so called **anti double-spend property**.  
  * The achievement of a *resilient and reliable* chronological ordering for distributed system, which embed important properties such as permissionlessness and censorship resistance, was reached by Satoshi Nakamoto with the invention of Bitcoin, using the blockchain data structure and a **Proof-of-Work** consensus which is able to entrust differrent participants to the system according to their computational power. Indeed Bitcoin can be considered to be the first working example of **Distributed Consensus System**.     

We will discuss various kind of **Distributed Consensus Systems** which have some degree of hierarchy and interrelated properties between them. They are differentiated on how they determine and enforce the most updated state of the system:
* **Blockchain + PoW Mechanism**. The sequence of **state transitions** is public and auditable and is organized in **transactions** included in ordered blocks which are added one upon the other. The security of the system lies on the amount of work required to produce an alternative chain which revert the actual greater-work chain which is considered as the valid chain. For instance **Bitcoin** is based on this technological stack.
* **State Channels**. Is a system constructed between 2 (or more) parties and which depend hierarchically on the blockchain layer. The final state is represented by the last transaction out of sequence of ordered invalidating transactions, signed and agreed by the parties *off-chain*. The final state can be enforced by each parties by publishing that last valid transaction on the layer 1. The most known application of state channels is the **Lightning Network**.
* **Client Side Validated Data - Stash**. Is a system that can be implemented both on top of blockchain and  state channels and it is based on a certain *circumscribed* amount data whose validity, computation tasks and update is entrusted to a *limited number* nodes. Differently form layer 1, the data to be validated by each client node represent a **defined subset of the entirery of all state transitions of the network, and NOT every transition happened within it**. This validated subset of data in possession of a client node is defined a **Stash** of the data. Basically, the client needs to validate the whole history of the state transitions occurred from the start to the last transition and which relate to the exchange and to the validation of some digital properties among the counterparties involved. Seen as a whole, the validation mechanism of the shard which produce the stash is called **Client-side Validation** and underpin all **RGB** operations.
 
![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/ac60cc0d-0d3f-4dbd-a7c5-2cef5ac1b765)  
*The 3 set of Distributed System - Blockchain (layer1) is self-sustaining while the other 2 rely on layer 1 for operating - layer 3 can operate on top of both blockchain and state channels*

In order to precisely frame the applications of each Distributed Consensus System and their undelying data structure it's important to understand the limitations that affect each one of these technology. This condition is expressed in form of a **Trilemma** which is connected to an important theoretical result of Distributed Computing, known as **[CAP Theorem](https://en.wikipedia.org/wiki/CAP_theorem)**. which states that:

> Any distributed data store can provide only two of the following three guarantees:
> * Consistency - Every read receives the most recent write or an error.
> * Availability - Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
> * Partition tolerance - The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/022ad2c0-f07d-4754-a3e6-a150bd64abdf)  
*Application of CAP Theorem to Distributed Consensus System - Each Distributed Consensus System can fit 2 and only 2 of the 3 properties*

Seen from a more consensus-focussed point of view, the properties of the theorem can be reformulated in the following way: 

* Consistency > Integrity
* Availability > Decentralization
* Parition Tollerance > Scalability and Confidentiality

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/7692116c-f13b-4a06-bb39-d649a0dce10c)  
*A more in-depth view of th inherent degree of application of the Trilemma to Distributed Consensus System*  

In syntesis:
* **Blockchain ** preserve Integrity and Decentralization but **lacks Scalability** and Confidentiality as each node need to replicate *publicly and in-full* every state transition.
* **State Channels** preserve Decentralization and Scalability but **doesn't preserve Integrity** as the state can be changed or updated asyncrnously by the counterparties.
* **Stashes of Client Side validated data** are Scalable and maintain Integrity, however they **are not replicated** by the vast majority of nodes of the network **lacking Availability**. For this reason these data are not decentralized as a single point of centralization which backup them is required to recover them in case of loss.  

An important feature to take into account is the different way through which State Channel and Client-Side validation architectures update the state of the data:

* State Channel state must be **syncronous** with the counterparties.
* Client side validated state update can be **asyncronous**

Naturally, if the client-side validated data are embedded in state channels, the update of the state will be ultimately based on an asyncronous process. 

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/aa3eecd6-4906-4bdd-8c5c-417edafabc70)

In addition to the 3 layers we have been just describing, a fourth layer of Bitcoin Finance (#BiFi) which laverages both state channels and blockchain can complete the whole ecosystem. The general picture and the deep inteconnections of all the layers, with the blockcain layer at the base, allow to achieve, in a composite way, all the properties of the CAP theorem.

In the next paragraph we will delve into Client-side Validation and its features.  

## Client-side Validation

The goal of every validation process of a distributed system machine is the **ability to assess the validity and the chronological ordering of the states**, hence to map the state transitions that took place.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/463eea67-d5e9-401c-916e-bce7357a538e)

In Bitcoin Blockchain, for instance, such process maps the change in the [UTXO set](https://en.wikipedia.org/wiki/Unspent_transaction_output) determined by the transactions collected into the sequence of ordered blocks. Thus, every block represent a **state update**.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/1d209128-de76-40ab-b291-373b1c74440a)

The main drawback of Layer 1 validation process is that **every node needs to validate store each transaction from everybody and store the related data** once block inclusion took place. This architecture lead to two main issues:
* Scalability: the size limit of the blocks vs. the demand of blockspace per unit time shared by all the participants willing to transact limit the transaction throughput (i.e. 1 MB on ~10 minutes on average on bitcoin)   
* Privacy: the detail of each transactions are broadcasted and stored in public form (in particular: the amounts transacted and the receiving adressess, although pseudonimous)
  
![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/403da928-31a8-4e08-8707-9c1f853df067)

However, from the point of view of a transaction recipient, the only aspects that matters are:
* the last state transition motivated by a transaction addrressed to him.
* the chronological sequence of transactions (and thus state transitions) that lead to that last state transition.

Basically what is important to him is the [Directed Acyclic Graph](#) which connect the history of the state transitions from the [genesis]() to the last state addressed to him (a **Shard** of the whole data)

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/6f81258f-1326-46e8-a951-16bc61163784)

For this reason, the **logic of validation can be reversed** in the following terms:
* Each party validates **its own part of the history** and thus the digital properties that matters to it.
* A compact reference of the **validated state transition is committed to the first layer** in order to be timestamped. This construction constitue a **Proof-of-Pubblication** and act as an **anti double-spend measure**. 

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/3c241331-abfa-42d9-af48-2d9bcb1aad33)

**Cliwent-side Validation ensure the respect of the following properties:
* Scalability: as the commitment of the verified state, which need to be stored by everyone, has a small size footprint (order on tens of byte)
* Privacy: by using a hash one-way function (such as SHA-256), the original data (the pre-image) which has produced the commitment cannot be reconstructed, and, in addition, they are kept private by the parties.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f429b7b9-2ddc-4701-94f0-296ce8144be0)

The commitment structure used in Client-side Validation (such as in RGB protocol which we will cover in depth later) allows important additional scalability features:
* aggregate state transitions of different properties (for example two different contracts pertaining to 2 different digital assets).
* bundle more than one state transition of the same asset in the same commitment.   

In order to guarentee the efficacy of the commitment scheme and a precise chronologica ordering stemmed from the blockchain layer, the use of a new cryptographic primitive needs to be introduced: the **Single-use Seal**.

## Single-use Seals

A Single-use seal is a form of **cryptographical commitment** which resemble that of the application of a physical seal to a box containing some objects, which allows to prove a sequence of events limiting the risk that this sequence of events can be altered after being set. This implies that such commitment scheme, [proposed](https://petertodd.org/2016/commitments-and-single-use-seals) by Peter Todd in ~2016, is more advanced than `simple commitments` and `timestamping`.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/984ef35b-6410-4eac-8163-d08b0ccc049e)

In order to work properly, Single-use seals require:

* a **Proof of Pubblication Medium**  - This can be a medium with global consensus (like blockchain layer) but not necessarily decentralized, for example a newspaper, which has the ability to be difficult to forge or replicate once issued and made public.
* to prove that a certain message `m` has been received by *every* member of a certain audience
* to prove that no other alternative medium has not been used to publish the message

With these properties we can state a more formal definition:

> A single-use Seal is a formal promise to commit to a (yet) unknown message in the future, once and only once, such that commitment fact will be provably known to all members of a certain audience.

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
 
In Seal definition, Alice promise to Bob (either in private or in public) to create some **message** (in practice an hash of some data):

* at a well definied point in time and space 
* using a precise pubblication medium

**Seal Closing**

When Alice publish the **message** following all the rules stated in the **seal definition**, in addition, she produces a **witness** which is the proof that the seal has been actually closed.  

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/3711069c-af89-494f-be31-dfeaa960d841)


**Seal Verification**
      
Once closed, the seal, being "single-use", cannot be opened nor closed again. The only thing that can be done by Bob, is to verify if the seal has been actually closed around the commitment of the message, using as inputs: the seal, the witness and the commitment (to the message).

In Computer Science Language the whole procedure can be summed-up as follows:
```
Define() -> seal  (done by Alice, accepted by Bob)

Close(seal, commitment(message)) -> witness    (close a seal over a message, done by Alice)

Verify(seal, witness, commitment(message)) ->  true|false  (verify that the seal was closed, done by Bob)
```

So the combination of single-use seals and client-side-validation allows for the creation of a distributed system that do not require global consensus (“blockchain”) in order to store all the data that matter to some counterparties, and this provide high level of scalability and privacy. However, this is not enough to make the system work. As the definition of a single-use seal is made on the client-side and it in not necessary to include it in the global consensus medium, **a party can’t prove that the definition of the seal has ever took place** even if you a member of audience observing the pubblication medium.

 `Thus we need a **“chain” of single-use-seals**, where **the seal closing of previous seal embedds the definition of the next seal(s): this is what RGB does together with Bitcoin**:
 * the messages are commitment to client-side validated data
 * the seal definitions are bitcoin UTXO
 * the commitment is an hash placed inside bitcoin transaction
 * the seal closing can be either an UTXO being spent or an addressed to which a transaction credit some bitcoins 

### Library for Client-side Validation
Repository:
* https://github.com/LNP-BP/client_side_validation

Rust Crates:
  * https://crates.io/crates/client_side_validation
  * https://crates.io/crates/single_use_seals
 
 In the next session we will explore in details how RGB implements the single use seal concept, storing commitments of its operation in the bitcoin blockchain.



 







[def]: image.png
