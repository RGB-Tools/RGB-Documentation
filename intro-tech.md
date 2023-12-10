# Technical Introduction

Before going entering into the technical details of the RGB, an introduction over the fundamental elements of the protocol, the environment undepinning the technological substrate, as well as the base terminology represent an essentia step towards a thorough understanding of the subject.

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
* **Client Side Validated Data (Layer 3)** Is a system that can be implemented on both blockchain and to state channels and it is based on a certain *limited* amount data whose validity, computation tasks and update is entrusted to each node. Differently form layer 1, the data to be validated by each client node represent **a defined subset of the entirery of all the state transition of the network**. This subset of data is often defined a **shard** of the data. Basically, the client needs to validate the whole history of the state transitions occurred from the start to the last transition and which relate the exchange of certain (digital) properties among the counterpary involved, and not any other data. This operation is called **Client-side Validation** and underpin all **RGB** operations.
 
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
* Client Side validated data (layer 3) are Scalable and maintin Integrity, however some data are not decentralized and hence lack Availability. Thus as single point of centralization of the data (e.g. the issuer) is required.  

An important feature to take into account is the different way through which State Channel and Client-Side validation architectures update the state of the data:

* State Channel state must be syncronous with the counterpary
* Client side validated state update can be asyncronous


# Client side Validated data


# Single Use Seals



