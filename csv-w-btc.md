# Layer 1 Anchoring

## Client-side Validation with Bitcoin

In this chapter we will explore the application of Client-Side-Validation and Single-Use-Seal to Bitcoin blockchain, introducing the main architectural features behind **RGB protocol**. As mentioned in the [previous chapter](broken-reference), these cryptographic operations can be applied in general to different blockchains and also to different publication media. However, the outstanding properties of Bitcoin consensus algorithm, particularly those related to decentralization, censorship resistance and permissionlessness, make it the ideal technology stack for the development of advanced programmability features, such as those required by digital bearer rights and smart contracts.

### Single-use Seals in Bitcoin Transactions and RGB

From the previous chapter, we recall that the creation of Single-use Seals is subject to two basic operations: **Seal Definition** and **Seal Closing**. We will now explore how these two operations can be implemented **using Bitcoin as a publication medium**, and in particular making use of some elements of the **Bitcoin Transactions**.

There are 2 main ways in which a Single-use Seal can be **defined** in Bitcoin transactions:

* **Public keys or addresses** - the seal is defined by selecting an address or public key that has not yet been used (i.e. it has not been used by any locking script, so it is not locking any bitcoin)
* **Bitcoin transaction outputs** – the seal is defined by the selection a specific UTxO available to some wallet.

The defined methods can be used in a combination of **closing methods** that differ according to how a **spending transaction**:

1. uses the seal definition: use of the address in the locking script or spending of the UTxO;
2. hosts the message on which the seal is closed according to a **commitment scheme** (i.e. in which part of the transaction the message is committed and stored).

The following table shows the 4 possible combinations of defining and closing the seal:

| Scheme name | Seal Definition        | Seal Closing           | Additional Requirements                        | Main application         | Possible commitment schemes |
| ----------- | ---------------------- | ---------------------- | ---------------------------------------------- | ------------------------ | --------------------------- |
| PkO         | Public key value       | Transaction output     | P2(W)PKH                                       | none yet                 | keytweak, tapret, opret     |
| **TxO2**    | **Transaction output** | **Transaction output** | **Requires Deterministic Bitcoin Commitments** | **RGBv1 (universal)**    | **keytweak, tapret, opret** |
| PkI         | Public key value       | Transaction input      | Taproot-only - Not working with legacy wallets | Bitcoin-based identities | sigtweak, witweak           |
| TxOI        | Transaction output     | Transaction input      | Taproot-only - Not working with legacy wallets | none yet                 | sigtweak, witweak           |

**RGB protocol uses the TxO2** scheme in which both seal definition and the seal closure use transaction outputs (the term "**O2**" in **TxO2** acronym stands for **2 Outputs**).

As shown in the table, several **commitment schemes** can be used for each **seal closing method**. Each method differs in the location used by related transactions to host the commitment and, in particular, whether the message is committed to a location belonging to the input or output of the transaction:

* Transaction Input:
  * Sigtweak - the commitment is placed within the 32-byte random **r** component that forms the ECDSA signature pair **\<r,s>** of an input. It make uses of [Sign-to-contract (S2C)](https://blog.eternitywall.com/2018/04/13/sign-to-contract/#sign-to-contract).
  * Witweak - commitment is placed within the segregated witness data of the transaction.
* Transaction Output (scriptPubKey):
  * Keytweak - It uses the [Pay-to-contract](https://blog.eternitywall.com/2018/04/13/sign-to-contract/#pay-to-contract) construction by which the public key of the output of the output is "tweaked" (i.e., modified) to contain a deterministic reference to the message.
  * **Opret** - The committed message is placed as an unspendable output after the opcode `OP_RETURN`.
  * **Tapret (taptweak)** - This scheme represents a form of tweak in which the message is committed to a string tagged `OP_RETURN` placed in a leaf of the `Script path` of a [taproot transaction](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) which then modifies the value of the PubKey.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/d0bc6d55-0918-48c1-b97d-73071f98874b)

### TxO2 Client-side Validation

In the next few paragraphs we will focus on client-side validation combined with the definition of a single-use seal and a **TxO2** scheme closure operation, showing them step by step below and using the two usual cryptographic characters: Alice, struggling with a seal operation, and Bob as an observer.

1. First of all, Alice has some UTxOs **that refer to data validated by the client and known only to her**.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/ad0684d1-294c-49e7-b80a-3ae6c5156a38)

2. Alice informs Bob that the spending of some UTxOs represents a sign that something has happened.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/c232438e-8571-492e-828d-d2c5e31760b8)

3. Once Alice spends her UTxO, only Bob knows that this expenditure has additional meaning, even though everyone (i.e., the Bitcoin blockchain audience) can see this event.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f770fd32-e903-49b0-a3ea-d604fd189770)

1. In fact, the UTxO spent by Alice through the **witness closure transaction** contains a commitment to the validated client-side data. By passing the original data to Bob, she is able to prove to Bob that this data is properly referenced by the commitment made by Alice in the spending transaction. The verification operation is performed by Bob independently, using the appropriate methods that are part of the client-side validation protocol (e.g., RGB protocol).

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f6440aae-202a-4569-bea7-f46664c00e92)

The key point of using the single-use seal in combination with client-side validation is the uniqueness of the spending event and the data committed (i.e., the message) in it, which cannot be changed in the future. The whole operation can be summarized in the following terms.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/dd575319-8eb8-48c2-837a-b6b7bf4faa81)

The next important step is to illustrate precisely how the two commitment schemes, **opret** and **tapret**, work and which are the features they must meet, particularly with regard to commitment determinism.

### Deterministic Bitcoin Commitment - DBC

For RGB commitment operations, the main requirement for a Bitcoin commitment scheme to be valid is that:

> The witness closing transaction must provably contain a single commitment.

With these requirements, it is not possible to construct an "alternate history" related to client-side data commitment in the same transaction. Thus, the message around which the single-use seal is closed is unique. To meet the requirement, regardless of the number of outputs in a transaction, _one and only one output_ is valid for each commitment scheme (opret and tapret):

> Uniqueness of RGB commitment: the only valid outputs that can contain an RGB message commitment are:
>
> 1. The first output OP\_RETURN (if present) for the `opret` commitment scheme.
> 2. The first taproot output (if present) for the `tapret` commitment scheme.

It is worth noting that a transaction can contain both a single `opret` and a single `tapret` commitment in two separate outputs. Of course, these commitments will commit to different client-side validated data which, as we shall see later, explicitly indicate the commitment method used to refer to themselves.

#### Opret

This is the simplest and most straightforward scheme. The commitment is inserted into the first output OP\_RETURN of the witness transaction in the following way:

```
34-byte_Opret_Commitment =
OP_RETURN OP_PUSHBYTE_32 <tH_MPC_ROOT>
|________| |___________| |____________|
  1-byte       1-byte       32 bytes                      
```

`tH_MPC_ROOT` is a 32-byte Tagged Multi Protocol Commitment (MPC) Merkle\_Root hash, so that the total commitment size in the _ScriptPubKey_ is 34 bytes.

#### Tapret

The Tapret scheme is a more complex form of deterministic commitment and is an improvement in terms of chain footprint and privacy of contract operations. The main idea of this application is to hide the commitment within the `Script path Spend` of a [taproot transaction](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki).

First, before showing how the commitment is actually embedded in a taproot transaction, we will show the exact **form of the commitment which is a 64-byte** string [constructed](https://github.com/BP-WG/bp-core/blob/master/dbc/src/tapret/mod.rs#L179-L196) as follows:

```
64-byte_Tapret_Commitment =

OP_RESERVED ...  ... .. OP_RESERVED  OP_RETURN  OP_PUSHBYTE_33  <tH_MPC_ROOT>  <Nonce>
|__________________________________| |________| |_____________| |____________| |______|
 OP_RESERVED x 29 times = 29 bytes     1 byte       1 byte         32 bytes    1 byte
|_____________________________________________________________| |_____________________|
        TAPRET_SCRIPT_COMMITMENT_PREFIX = 31 bytes               MPC commitment + NONCE = 33 bytes
```

Thus the 64-byte `tapret` commitment is an `Opret` commitment preceded by 29 bytes of the OP\_RESERVED operator and to which is added a 1-byte `Nonce` whose usefulness will be addressed [later](csv-w-btc.md#nonce-optimization).

In order to preserve highest degree of implementation flexibility, privacy and scalability, **the Tapret scheme is designed to integrate many different cases that occur according to the user's bitcoin spending needs**, specifically we distinguish the following Tapret scenarios:

* **Single incorporation** of RGB Tapret commitment into a taproot transaction **without Script Path Spend structure**.
* **Integrate** of Tapret RGB commitment into a taproot transaction containing a **pre-existing Script Path Spend structure**.

We will analyze each of these scenarios below.

**Tapret Incorporation without Script Path Spend**

To show this first scenario, the standard of a taproot exit key `Q` consisting only of an internal key `P` and **no Spending script path** is shown below

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
                    +-------------+
                    | tH_TWEAK(P) |
                    +-------------+
```

* `P` is the Internal Public Key of the _Key Path Spend_
* `G` is the Generator point of secp256k1 curve
* `tH_TWEAK(P)` = SHA-256(SHA-256(_TapTweak_) || SHA-256(_TapTweak_) || P) which makes use of [BIP86](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki#address-derivation) to show that there is no Script Path Spend

To include tapret commitment in such a transaction, we modify the transaction to provide the commitment as a single script, according to the following scheme:

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
             +----------------------------+
             | tH_TWEAK(P || Script_root) |
             +---------------------^------+
                                   |
         +-------------------------+------------+
         | tH_BRANCH(64-byte_Tapret_Commitment) |
         +--------------------------------------+
```

* `P` is the Internal Public Key of the _Key Path Spend_
* `G` is the Generator point of secp256k1 curve
* `m` is the tweaking hash
* `tH_TAG(x)` = TaggedHash("tag\_id",x) = SHA-256(SHA-256(_tag\_id_) || SHA-256(_tag\_id_) || x)
  * `tH_TWEAK(x)` = SHA-256(SHA-256(_TapTweak_) || SHA-256(_TapTweak_) || x)
  * `tH_BRANCH(x)` = SHA256(SHA-256(_TapBranch_) || SHA-256(_TapBranch_) || x)

The proof of inclusion and uniqueness in the Taproot Script tree is only the internal key `P`.

**Tapret incorporation in pre-existing Script Path Spend**

To move on to the construction of this more complex case, we show below the structure of a taproot output Key `Q`, which in this example consists of a Spend Key Path with internal key `P` and a 3-script tree in the Spend Script Path.

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
             +----------------------------+
             | tH_TWEAK(P || Script_root) |
             +---------------------^------+
                                   |
                     +-------------+----------+
                     | tH_BRANCH(tHAB || tHC) |
                     +------------^-------^---+
                                  |       |
                        +---------+       +---------+
                        |                           |
           +------------+----------+         +------+-----+
           | tH_BRANCH(tHA || tHB) |         | tH_LEAF(C) |
           +------------^------^---+         +------^-----+
                        |      |                    |
                 +------+      +------+             |
                 |                    |             |
           +-----+------+       +-----+------+      | 
           | tH_LEAF(A) |       | tH_LEAF(B) |      |
           +-----^------+       +-----^------+      |
                 |                    |             | 
               +-+-+                +-+-+         +-+-+
               | A |                | B |         | C |
               +---+                +---+         +---+
```

Where:

* `tH_TAG(x)` = TaggedHash("tag\_id",x) = SHA-256(SHA-256(_tag\_id_) || SHA-256(_tag\_id_) || x)
  * `tH_LEAF(x)` = SHA-256(SHA-256(_TapLeaf_) || SHA-256(_TapLeaf_) || version\_leaf(x) || size(x) || x)
* `A, B, C` are some Bitcoin scripts of this Taproot Tree

The RGB Tapret commitment rule imposes the following requirements:

1. **Tapret Commitment is entered as an unspendable script at the 1st level of the Script Tree, shifting all other scripts 1 level below.**

The new Taproot Output Key `Q` including the tapret commitment is built as follows:

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
                           +--------------------+
                                                |
                                +---------------+------------+
                                | tH_TWEAK(P || Script_root) |
                                +---------------------^------+
                                                      |
                                       +--------------+----------+
                                       | tH_BRANCH(tHABC || tHT) |
                                       +-------------^-------^---+
                                                     |       |
                     +-------------------------------+       +-------+
                     |                                               |
          +----------+-------------+               +-----------------+--------------------+
          | tH_BRANCH(tHAB || tHC) |               | tH_BRANCH(64_byte_Tapret_Commitment) |
          +------------^-------^---+               +--------------------------------------+
                       |       |
             +---------+       +-----------+
             |                             |
+------------+----------+           +------+-----+
| tH_BRANCH(tHA || tHB) |           | tH_LEAF(C) |
+------------^------^---+           +------^-----+
             |      |                      |
      +------+      +------+               |
      |                    |               |
+-----+------+       +-----+------+        |
| tH_LEAF(A) |       | tH_LEAF(B) |        |
+-----^------+       +-----^------+        |
      |                    |               |
    +-+-+                +-+-+           +-+-+
    | A |                | B |           | C |
    +---+                +---+           +---+
```

2. According to Taproot rules, **every branch and leaf hashing operation is performed in lexicographic order of the two operands**. Therefore, two cases can occur that lead to two different proofs of uniqueness of commitment:
   1. If the hash of the tapret commitment (`tHT`) **is greater** than the top-level hash of the Script Path Spend (`tHABC`), it will be put on **the right side of Script Tree**. In this case, according to the rules of the RGB protocol, the commitment at this position is considered a valid proof of uniqueness and the Merkle Proof of the inclusion and uniqueness of commitments consists of only `tHABC` and `P`.
   2. If the hash of the tapret commitment (`tHT`) **is smaller** than the top-level hash of the Script Path Spend (`tHABC`), it will be placed on **the left side of the Script Tree**. In this case, it is necessary to show that there are no other tapret commitments on the right side of the Tree. To do this, `tHAB` and `tHC` must be revealed and form the merkle proof of inclusion and uniqueness along with `P`.

&#x20;

* **`tHABC < tHT`**

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
                           +--------------------+
                                                |
                                +---------------+------------+
                                | tH_TWEAK(P || Script_root) |
                                +---------------------^------+
                                                      |
                                       +--------------+----------+
                                       | tH_BRANCH(tHABC || tHT) |
                                       +-------------^-------^---+
                                                     |       |
                     +-------------------------------+       +-------+
                     |                                               |
          +----------+-------------+               +-----------------+--------------------+
          | tH_BRANCH(tHAB || tHC) |               | tH_BRANCH(64_byte_Tapret_Commitment) |
          +------------------------+               +--------------------------------------+
```

&#x20;

* **`tHABC > tHT`**

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
                           +--------------------+
                                                |
                                +---------------+------------+
                                | tH_TWEAK(P || Script_root) |
                                +---------------------^------+
                                                      |
                                       +--------------+----------+
                                       | tH_BRANCH( tHT || tHABC)|   
                                       +-------------^-------^---+
                                                     |       |
                                  +------------------+       +------------------+
                                  |                                             |
             +--------------------+-----------------+              +------------+-----------+
             | tH_BRANCH(64_byte_Tapret_Commitment) |              | tH_BRANCH(tHAB || tHC) |
             +--------------------------------------+              +------------^-------^---+
                                                                                |       |
                                                                   +------------+       +--------+
                                                                   |                             |
                                                      +------------+----------+           +------+-----+
                                                      | tH_BRANCH(tHA || tHB) |           | tH_LEAF(C) |
                                                      +-----------------------+           +------------+
```

**Nonce optimization**

As an additional optimization method, the `<Nonce>` representing the last byte of the `64_byte_Tapret_Commitment` allows the user constructing the proof to attempt at "mining" a `tHT` such that `tHABC < tHT`, thus placing it in the right-hand side of the tree and definitely avoiding revealing the constituents of the script branch (in this example `tHaB` and `tHC`)

### Multi Protocol Commitment - MPC

Multi Protocol commitments address the following important requirements:

1. How the tagged value which is committed is constructed according to `opret` or `tapret` schemes.
2. How state changes associated with more than one contract can be stored in a single commitment.

In practice, the preceding points are addressed through an **ordered merkelization** of the multiple contracts/state transitions associated with the UTxO that are expended by the **witness closing transaction** where such multiple transitions are eventually committed by means of DBC.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/db6c410c-9ce1-4575-b0b4-e7c09f38d502)

#### MPC Tree root

The root of the MPC tree,, which goes either into [opret](csv-w-btc.md#opret) or into [tapret](csv-w-btc.md#tapret) commitment is the `tH_MPC_ROOT(x)` constructed in BIP-341 fashion as follows:

`tH_MPC_ROOT(x) = SHA-256(SHA-256(urn:lnpbp:lnpbp0004:tree:v01#23A) || SHA-256(urn:lnpbp:lnpbp0004:tree:v01#23A) || x)`

#### MPC Tree Construction

In order to construct the MPC tree we must **deterministically provide a position of the leaf belonging to each contract**, thus:

> By setting `C` the number of contracts `c_i` to be included in the MPC we can construct a tree with `w` leaves with `w > C` (corresponding to a depth `d` such that `2^d = w`), such that each contract identifier `c_i` representing a different contract is placed in unique position `pos_i = c_i mod w`

In essence, the construction a suitable tree of width `w` that hosts each contract `c_i` in a unique position represents a kind of mining process. The greater the number of contract `C`, the greater should be the number of leaves `w`. Assuming a random distribution of `pos_i`, as per [Birthday Paradox](https://en.wikipedia.org/wiki/Birthday\_problem), we have \~50% probability of a collision occurring at the position in a tree with `w ~ C^2`.

To avoid too large MPC trees and the occurrence of collisions being a random process, an additional optimization was introduced. The modulus operation was modified according to the following formula: `pos_i = c_i + cofactor mod w` where `cofactor` is a random number of 16 bytes that can be chosen as a "nonce" to obtain distinct values of `pos_i` with `w` fixed. The tree construction process starts from the smallest tree such that `w > C`, then tries a certain number of `cofactor` attempts, if none of them can produce `C` distinct positions, `w` is increased and a new series of `cofactor` trials is attempted.

**Contract Leaves (Inhabited)**

Once `C` distinct positions `pos_i` with `i = 0,...,C-1` are found, the corresponding leaves are populated in the following way:

`tH_MPC_LEAF(c_i) = SHA-256(SHA-256(urn:lnpbp:lnpbp4) || SHA-256(urn:lnpbp:lnpbp4) || 0x10 || c_i || BUNDLE_i )`

Where:

* `0x10` is the integer identifier of contract leaves;
* `c_i` is the 32-byte contract\_id which is the hash of the [genesis](csv-w-btc.md) of the contract itself;
* `BUNDLE_i` is the 32-byte hash that is calculated from the data of the bundle of state transition.

**Entropy leaves (Uninhabited)**

For the remaining `w - C` uninhabited leaves, a dummy value must be committed. In order to do that, each leaf in position `j != pos_i` is populated in the following way:

`tH_MPC_LEAF(j) = SHA-256(SHA-256(urn:lnpbp:lnpbp4) || SHA-256(urn:lnpbp:lnpbp4) || 0x11 || entropy || j )`

Where:

* `0x11` is the integer identifier of entropy leaves;
* `entropy` is a 64-byte random value chosen by the user constructing the tree.

The following diagram shows the construction of an example MPC tree where:

* `C = 3`
* `d = 3 (w = 8)`
* `tH_MPC_BRANCH(tH1 || tH2) = SHA-256(SHA-256(urn:lnpbp:lnpbp4) || SHA-256(urn:lnpbp:lnpbp4) || d || w || tH1 || tH2)`
* `d` and `w` is the tree depth and width respectively
* `pos_1 = 7, pos_2 = 4, pos_3 = 2`

```
                                                                                   +-------------------------------+
                                                                                   | tH_MPC_ROOT(tHABCD || tHEFGH) |
                                                                                   +----------------^---------^----+
                                                                                                    |         |
                                              +-----------------------------------------------------+         +---------------------------------------+
                                              |                                                                                                       |
                                +-------------+---------------+                                                                         +-------------+---------------+
                                | tH_MPC_BRANCH(tHAB || tHCD) |                                                                         | tH_MPC_BRANCH(tHEF || tHGH) |
                                +----------------^--------^---+                                                                         +-----------------+--------+--+
                                                 |        |                                                                                               |        |
                     +---------------------------+        +--------------+                                                   +------------------<---------+        +------------+
                     |                                                   |                                                   |                                                  |
       +-------------+-------------+                       +-------------+-------------+                       +-------------+-------------+                      +-------------+-------------+
       | tH_MPC_BRANCH(tHA || tHB) |                       | tH_MPC_BRANCH(tHC || tHD) |                       | tH_MPC_BRANCH(tHE || tHF) |                      | tH_MPC_BRANCH(tHG || tHH) |
       +----------------^------^---+                       +----------------^------^---+                       +----------------^------^---+                      +----------------^------^---+
                        |      |                                            |      |                                            |      |                                           |      |
         +--------------+      +-----+                       +--------------+      +- ---+                       +--------------+      + ----+                      +--------------+      +-----+
         |                           |                       |                           |                       |                           |                      |                           |
 +-------+--------+        +---------+------+        +-------+--------+        +---------+------+        +-------+--------+        +---------+------+        +------+---------+        +--------+-------+
 | tH_MPC_LEAF(A) |        | tH_MPC_LEAF(B) |        | tH_MPC_LEAF(C) |        | tH_MPC_LEAF(D) |        | tH_MPC_LEAF(E) |        | tH_MPC_LEAF(F) |        | tH_MPC_LEAF(G) |        | tH_MPC_LEAF(H) |
 +-------------^--+        +-------------^--+        +-------------^--+        +-------------^--+        +-------------^--+        +-------------^--+        +-------------^--+        +-------------^--+
               |                         |                         |                         |                         |                         |                         |                         | 
+--------------+-------+  +--------------+-------+  +--------------+----------+  +-----------+---------+  +------------+------------+  +---------+------------+  +---------+------------+  +---------+---------------+ 
| 0x11 || entropy || 0 |  | 0x11 || entropy || 1 |  | 0x10 || c_3 || BUNDLE_3 |  | 0x11 | entropy || 3 |  | 0x10 || c_2 || BUNDLE_2 |  | 0x11 || entropy || 5 |  | 0x11 || entropy || 6 |  | 0x10 || c_1 || BUNDLE_1 | 
+----------------------+  +----------------------+  +-------------------------+  +---------------------+  +-------------------------+  +----------------------+  +----------------------+  +-------------------------+
```

#### MPC Tree Verification

From a verifier's perspective, in order to prove the presence of client-side validate related to some contract `c_i` collected in BUNDLE\_i, **only a **_**Merkle Proof**_** pointing at it inside the tree is needed**. Because of this, different verifiers of different contracts do not have the full view of the Merkle Tree as the builder does, and this guarantee, together with the dummy entropy, leaves a high degree of privacy. Using the example tree in the diagram above, a verifier of, say, the contract `c_3` will receive the following _Merkle Proof_ from the tree builder:

```
                                                                            +-------------------------------+
                                                                            | tH_MPC_ROOT(tHABCD || tHEFGH) |
                                                                            +----------------^---------^----+
                                                                                             |         |
                                       +-----------------------------------------------------+         +---------------------------------------+
                                       |                                                                                                       |
                         +-------------+---------------+                                                                         +-------------+---------------+
                         | tH_MPC_BRANCH(tHAB || tHCD) |                                                                         | tH_MPC_BRANCH(tHEF || tHGH) |
                         +----------------^--------^---+                                                                         +-----------------------------+
                                          |        |
              +---------------------------+        +--------------+
              |                                                   |
+-------------+-------------+                       +-------------+-------------+
| tH_MPC_BRANCH(tHA || tHB) |                       | tH_MPC_BRANCH(tHC || tHD) |
+----------------^------^---+                       +----------------^------^---+
                                                                     |      |
                                                      +--------------+      +- ---+
                                                      |                           |
                                              +-------+--------+        +---------+------+
                                              | tH_MPC_LEAF(C) |        | tH_MPC_LEAF(D) |
                                              +-------------^--+        +-------------^--+
                                                            |                         |
                                             +-------------------------+  +------+----+---------+                                                                                                           
                                             | 0x10 || c_3 || BUNDLE_3 |  | 0x11 | entropy || 3 |                                                                                                           
                                             +-------------------------+  +------+--------------+                                                                                                           
```

So the Merkle Proof provided to verify the existence and uniqueness of contract commitment in the tree is: `0x11 | entropy || 3` `tH_MPC_BRANCH(tHA || tHB)` `tH_MPC_BRANCH(tHEF || tHGH)`.

## Anchors

Anchors are the client-side validated structure that summarizes all the data needed to validate contract commitments, which were described earlier in this section. They are structured as follows:

`Txid` `MPC Proof` `DBC Proof`

Where:

* `Txid` is the 32-byte Bitcoin Transaction Id which contains the data-related `opret` `tapret` commitment. Note that `TxId` could theoretically be reconstructed from the off-chain data of state transitions pointing to each on-chain closing transaction, however for simplicity they are included in the anchor.
* The `MPC Proof` of the contract `c_i` consists of `pos_i` `cofactor` `Merkle Proof` which were described above.
* `DBC Proof`:
  * If an `opret` commitment is used, no additional proof is provided, since, as described above, the verifier inspects the first `OP_RETURN` output finding the correct `tH_MPC_ROOT`.
  * If a `tapret` commitment is used, a so called **Extra Transaction Proof - ETP** must be provided, which consists of:
    * Internal Public Key `P` of the Taproot output used.
    * Partner node(s) of the `Taproot Script Path Spend` which is either:
      * The top left branch (in the example `tHABC`) if the `tapret` commitment is on the right side of the tree.
      * The left and right nodes of the upper right branch (in the example `tHAB` and `tHC`) if the `tapret` commitment is on the left side of the tree.
    * The `nonce`, if used, to optimize the Partner node part of the proof.

#### Library for Client-side Validation and Deterministic Bitcoin Commitments

Repository:

* https://github.com/LNP-BP/client\_side\_validation

Rust Crates:

* https://crates.io/crates/rgb-core
* https://crates.io/crates/client\_side\_validation
* https://crates.io/crates/bp-dbc

In the next chapter we will introduce concepts purely concerning the off-chain part of RGB, i.e., contracts, giving an abstract view of the partially replicated finite state machine that gives RGB a much greater expressiveness than can be achieved through Bitcoin Script without sacrificing confidentiality.
