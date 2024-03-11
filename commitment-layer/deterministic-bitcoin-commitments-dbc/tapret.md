# Tapret

The `Tapret` scheme is a more complex form of deterministic commitment and represents an improvement in terms of chain footprint and privacy of contract operations. The main idea of this application is to hide the commitment within the `Script Path Spend` of a [taproot transaction](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki).

First, before describing how the commitment is actually embedded in a taproot transaction, we will show the exact **form of the commitment which must match exactly a 64-byte string size** [constructed](https://github.com/BP-WG/bp-core/blob/master/dbc/src/tapret/mod.rs#L179-L196) as follows:

```
64-byte_Tapret_Commitment =

 OP_RESERVED ...  ... .. OP_RESERVED   OP_RETURN   OP_PUSHBYTE_33  <mpc::Commitment>  <Nonce>
|___________________________________| |_________| |______________| |_______________|  |______|
 OP_RESERVED x 29 times = 29 bytes      1 byte         1 byte          32 bytes        1 byte
|________________________________________________________________| |_________________________|
        TAPRET_SCRIPT_COMMITMENT_PREFIX = 31 bytes                    MPC commitment + NONCE = 33 bytes
```

Thus the 64-byte `Tapret` commitment is an `Opret` commitment preceded by 29 bytes of the `OP_RESERVED` operator and to which is added a 1-byte `Nonce` whose usefulness will be addressed [later](tapret.md#nonce-optimization).

In order to preserve highest degree of implementation flexibility, privacy and scalability, **the Tapret scheme is designed to integrate many different cases that occur according to the user's bitcoin spending needs**. Specifically we distinguish the following Tapret scenarios:

* **Single incorporation** of a Tapret commitment into a taproot transaction **without Script Path Spend structure**.
* **Integration** of a Tapret commitment into a taproot transaction **containing a pre-existing Script Path Spend structure**.

We will analyze each of these scenarios in depth in the next paragraphs.

## **Tapret Incorporation without Script Path Spend**

In this first scenario, a Taproot Output Key `Q` consisting only of an Internal Key `P` and **no Spending script path** is reported below:

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
                    +-------------+
                    | tH_TWEAK(P) |
                    +-------------+
```

* `P` is the Internal Public Key of the _Key Path Spend._
* `G` is the Generator point of secp256k1 curve.
* `tH_TWEAK(P)` = SHA-256(SHA-256(_TapTweak_) || SHA-256(_TapTweak_) || P) which makes use of [BIP86](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki#address-derivation) to show that there is no Script Path Spend.

To include Tapret commitment in such a transaction, the transaction is modified in order to provide the commitment as a single script, according to the following scheme:

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

* `P` is the Internal Public Key of the _Key Path Spend._
* `G` is the Generator point of secp256k1 curve.
* `m` is the tweaking hash.
* `tH_TAG(x)` = TaggedHash(_tag\_id_, x) = SHA-256(SHA-256(_tag\_id_) || SHA-256(_tag\_id_) || x)
  * `tH_TWEAK(x)` = SHA-256(SHA-256(_TapTweak_) || SHA-256(_TapTweak_) || x)
  * `tH_BRANCH(x)` = SHA256(SHA-256(_TapBranch_) || SHA-256(_TapBranch_) || x)

The proof of inclusion and uniqueness in the Taproot Script Tree is only the internal key `P`.

## **Tapret incorporation in pre-existing Script Path Spend**

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

* `tH_TAG(x)` = TaggedHash(_tag\_id_, x) = SHA-256(SHA-256(_tag\_id_) || SHA-256(_tag\_id_) || x).
  * `tH_LEAF(x)` = SHA-256(SHA-256(_TapLeaf_) || SHA-256(_TapLeaf_) || version\_leaf(x) || size(x) || x).
* `A, B, C` are some Bitcoin scripts of this Taproot Tree.

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
   2. If the hash of the tapret commitment (`tHT`) **is smaller** than the top-level hash of the Script Path Spend (`tHABC`), it will be placed on **the left side of the Script Tree**. In this case, it is necessary to show that there are no other tapret commitments on the right side of the Tree. To do this, `tHAB` and `tHC` must be revealed and form the Merkle proof of inclusion and uniqueness along with `P`.

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

## **Nonce optimization**

As an additional optimization method, the `<Nonce>` representing the last byte of the `64_byte_Tapret_Commitment` allows the user constructing the proof to attempt at "mining" a `tHT` such that `tHABC < tHT`, thus placing it in the right-hand side of the tree and definitely avoiding revealing the constituents of the script branch (in this example `tHAB` and `tHC`).

***
