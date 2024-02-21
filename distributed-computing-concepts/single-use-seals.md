# Single-use Seals and Proof of Pubblication

Single-Use seals are cryptographic primitives [proposed](https://petertodd.org/2016/commitments-and-single-use-seals) by Peter Todd in \~2016. They are a kind of **cryptographic commitment** that resembles the application of a physical seal to a container. They can be used to prove a sequence of events to a party, thereby limiting the risk that this sequence of events may be altered after it has been established. This implies that such commitment schemes are a more sophisticated form of both `simple commitments` (i.e. digest/hash) and `timestamping`.\


<figure><img src="../.gitbook/assets/physical-single-use-seals.png" alt=""><figcaption><p><strong>Physical single-use seals: once closed their protected content cannot be altered</strong></p></figcaption></figure>

In order to work properly, Single-Use-Seals require a **Proof-of-Publication Medium**: it may be a medium with global consensus (such as blockchain) but not necessarily decentralized which has the ability to be difficult to forge or replicate once issued and made public, such as a newspaper.

The **Proof-of-Publication Medium** will be used:

* to prove that _every_ member `p` in a audience `P` has received message `m`;
* to prove that message `m` has not been published;
* to prove that some member `q` is in the audience `P`.

With these properties we can give a more formal definition:

> _Single-Use-Seal is a formal promise to commit to a (yet) unknown message in the future, once and only once, such that the fact of commitment is demonstrably known to all members of a certain audience._

With this definition and the general properties above, we can compare the properties of the various cryptographic primitives mentioned with Single-Use-Seals:

|                                                                      | Simple commitment (digest/hash) | Timestamps   | Single-Use-Seals |
| -------------------------------------------------------------------- | ------------------------------- | ------------ | ---------------- |
| Commitment publication does not reveal the message                   | Yes                             | Yes          | Yes              |
| Proof of the commitment time / message existence before certain date | Not Possible                    | Possible     | Possible         |
| Prove that no alternative commitment can exist                       | Not Possible                    | Not Possible | Possible         |

So how can we practically construct a disposable seal and what can be used? In general, the principles of operation include 3 steps:

* Seal Definition;
* Seal Closing;
* Seal Verification.

For the examples we will use the well-known computer science characters, Alice and Bob.

### **Seal Definition**

In Seal definition, Alice promise to Bob (either in private or in public) to create some **message** (in practice an hash of some data):

* at a well-defined point in time and space;
* using an agreed publication medium.

### **Seal Closing**

When Alice publishes the **message** following all the rules stated in the **seal definition**, in addition, she produces also a **witness**, which is the proof that the seal has indeed been closed.

<figure><img src="../.gitbook/assets/closed-single-use-seal.png" alt=""><figcaption><p><strong>By closing a message with a single-use seal, such message cannot be altered. In it's digital form inscribed in Layer 1, the seal cannot be opened any more</strong></p></figcaption></figure>

### **Seal Verification**

Once closed the seal, being "single-use", cannot be opened nor closed again. The only thing Bob can do is to check whether the seal has actually been closed around the message commitment, using as inputs: the seal, the witness and the commitment (to the message).

In Computer Science Language the whole procedure can be summed-up as follows:

```
seal <- Define()                         # Done by Alice, accepted by Bob.

witness <- Close(seal, message)          # Close a seal over a message, done by Alice.

bool <- Verify(seal, witness, message)   # Verify that the seal was closed, done by Bob.
```

The combination of Single-Use-Seals and Client-Side-Validation enables a distributed system that does not require global consensus (i.e. a blockchain) to store all the data that matters to some counterparts, providing a high level of scalability and privacy. However, this is not enough to make the system work. Because the definition of a Single-Use-Seal is done on the client side and does not need to be included in the global consensus medium, **a party can’t prove that the definition of the seal ever took place** even if one is a member of the audience observing the publication medium.

We therefore need a **“chain” of Single-Use-Seals**, where **the closure of the previous seal incorporates the definition of subsequent seal(s): this is what RGB does together with Bitcoin**:

* messages are committed to client-side validated data;
* seal definitions are bitcoin UTXO;
* the commitment is a hash entered within a Bitcoin transaction;
* the seal closure can be a UTXO that is spent or an address to which a transaction credits some bitcoin.

## Libraries for Client-side Validation

Repository:

* https://github.com/LNP-BP/client\_side\_validation

Rust Crates:

* https://crates.io/crates/client\_side\_validation
* https://crates.io/crates/single\_use\_seals

In the next chapters we will explore in detail how RGB implements the concept of Single-Use-Seal by storing the commitments of its operation in the Bitcoin blockchain.
