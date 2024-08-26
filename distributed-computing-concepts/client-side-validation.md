# Client-side Validation

The goal of every validation process in a distributed system is the **ability to assess the validity and chronological ordering of states**, hence to verify the correctness with respect to the protocol rules of the state transitions that have occurred.

<figure><img src="../.gitbook/assets/state-passages.png" alt=""><figcaption><p><strong>Consensus system allows for the tracking of the state evolution of some properties</strong></p></figcaption></figure>

In Bitcoin Blockchain, for instance, this process is meant to verify the correctness of the changes in the [UTXO set](https://en.wikipedia.org/wiki/Unspent\_transaction\_output) determined by the transactions collected into the sequence of ordered blocks. Thus, every block represents a **state update**.

<figure><img src="../.gitbook/assets/utxo-set-1.png" alt=""><figcaption><p><strong>In Bitcoin the System State is represented by the UTXO Set, reflecting the ownership of bitcoins.</strong></p></figcaption></figure>

The main drawback of Layer 1 validation process is that **each node has to validate each transaction from everybody and store the related data** once block inclusion takes place. This architecture leads to two main issues:

* **Scalability**: the size limit of the blocks vs. the demand of blockspace per unit time shared by all willing participants limits the transaction throughput (i.e. a maximum of 1 MB on \~10 minutes on average on bitcoin, taking into account [witness discount](https://en.bitcoin.it/wiki/Segregated\_Witness)).
* **Privacy**: details of each transaction are broadcasted and stored in public form (in particular: the amounts transacted and the receiving addresses, although pseudonyms).

<figure><img src="../.gitbook/assets/blockchain-1.png" alt=""><figcaption><p><strong>In Public Blockchains everyone needs to validate all the information leading to privacy and scalability issues.</strong></p></figcaption></figure>

However, from the point of view of the recipient of a transaction, the only aspects that matter are:

* The last state transition motivated by a transaction addressed to him.
* The chronological sequence of transactions (and thus state transitions) leading up to the last state transition.

Basically, what is relevant to the recipient is the [Directed Acyclic Graph](../annexes/glossary.md#directed-acyclic-graph-dag) which connects the history of the state transitions from the [Genesis](../annexes/glossary.md#genesis) to the last state addressed to him (a [Shard](../annexes/glossary.md#shard) of the whole data).

<figure><img src="../.gitbook/assets/transaction-graph-1.png" alt=""><figcaption><p><strong>The transaction graph of Public Blockchains cannot be sharded due to internal consistency.</strong></p></figcaption></figure>

For this reason, the **logic of validation can be reversed** in the following terms:

* Each part validates its **own part of the history** and thus the digital properties that matters to him.
* A compact reference of the **validated state transition is committed in the 1st layer** to be timestamped. This construction constitutes a [Proof-of-Publication](https://petertodd.org/2017/scalable-single-use-seal-asset-transfer) and acts as an **anti double-spending measure**.

<figure><img src="../.gitbook/assets/csv-blocks-1.png" alt=""><figcaption><p><br><strong>The Layer 1's blocks are kept public, but client-side validated state transition are aggregated and committed through suitable merkelization in Layer 1's transactions.</strong></p></figcaption></figure>

**Client-side Validation** ensures that the following properties are met:

* **Scalability**: since the commitment of the verified state, which must be stored by all, has, at least, a small footprint (order of tens of bytes), or, in [some commitment scheme](../commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md), no additional footprint in respect to an ordinary transaction.
* **Privacy**: using a [one-way cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic\_hash\_function) (such as [SHA-256](https://en.wikipedia.org/wiki/SHA-2)), the original data (the pre-image) that produced the commitment cannot be reconstructed and, moreover, it is kept private by the parties.

<figure><img src="../.gitbook/assets/csv-shard-1.png" alt=""><figcaption><p><strong>Several shards can be aggregated in a single Layer 1 transaction. The Anchor structure establish a link between the client-side data of the contract and the single-use seal.</strong> </p></figcaption></figure>

The commitment structure used in Client-Side Validation (as in the RGB protocol, which we will cover in detail [later](../commitment-layer/commitment-schemes.md)) allows for important additional scalability features:

* Aggregate state transitions of different contracts (e.g., two different contracts related to 2 different digital assets committed in a single bitcoin transaction).
* Bundle more than one state transition of the same asset in the same client-side operation.

[Anchor](../commitment-layer/anchors.md) structures provide the deterministic link between the [single-use seal](single-use-seals.md) and the client-side data that represent the message to which the [single-use seal is closed around](single-use-seals.md#seal-closing). &#x20;

In order to guarantee the efficacy of the commitment scheme and precise chronological ordering derived from the 1st layer, the use of a new cryptographic primitive needs to be introduced: the **Single-use Seal**.

***
