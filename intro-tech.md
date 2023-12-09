# Technical Introduction

Before going entering into the technical details of the RGB, an introduction over the fundamental elements of the protocol, the environment undepinning the technological substrate, as well as the base terminology represent an essentia step towards a thorough understanding of the subject.

## Paradigm of Distributed Computing

* RGB locate itself as an additional piece of the ample word of *Distributed Computing*.
* Distributed computing, is a branch of Computer Science which study the protocol systems able to exchange and compute data information between of a network of computer nodes: the set of computer nodes and the undelying protocol rules which allows the computation are the contituents of the **Distributed system**.  
  * The nodes, composing the network are able to indipendently verify and validate such set of data and they can contruct, depending on the protocol, complete or partial snapshots of the properties of the network: these are **state** of the distributed system and essentially represent the expression of properties and agreement that took place in network operations.
  * The most important properties of a Distributed Systems is represented by the **chronological ordering** of the operations and thus the **ordered sequence of state changes** that take place inside the system. In fact when we talk about **Consensus**, we are talking about the **re cognized validity of the state transitions** by the nodes and most importantly about the **consensus on the order of the state transitions** so that every node knows which state precedes the other.
  * The achievement of a *resilient and reliable* chronological ordering for distributed system, which embed important properties such as permissionlessness and censorship resistance, was reached by Satoshi Nakamoto with the invention of Bitcoin, using the blockchain data structure and a Proof-of-Work consensus which is able to entrust differrent participants to the system according to their computational power.     
* We will discuss a particular **set of distributed systems** which have some degree of hierarchy and interrelated properties and which in the current context are based on based on Bitcoin but can be teorethically extended to other system. They are differentiated on how to dermenine and enforce the most updated state of the system:
  * **Blockchain /Timechain + PoW Mechanism (layer 1)**. The sequence of **state transitions** is public and auditable and is organized in **transaction** included in ordered blocks which are added one upon the other. The security of the system lies on the amount of work required to produce an alternative chain which revert the actual greater-work chain which is considered as the valid chain.
  * **State channels (layer 2)**. Is a system constructed between 2 (or more) parties and which depend hierarchically on layer 1. The final state is represented by the last transaction out of sequence of ordered invalidating transactions, signed and agreed by the parties *off-chain*. The final state can be enforced by each parties by publishing that last valid transaction on the layer 1.
  * **Client Side Validated Data (layer3?)** Is a system that can be implemented on both blockchain and to state channels and is based on a certain amount of data which 
  * 
![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/ac60cc0d-0d3f-4dbd-a7c5-2cef5ac1b765)


# Single Use Seals



