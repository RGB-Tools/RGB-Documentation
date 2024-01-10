# Client-side Validation with Bitcoin

In this section we will explore the application of client-side validation and single-use seal to Bitcoin Blockchain, introducing the main architectural features behind **RGB protocol**.
As mentioned in the [previous chapter](intro-tech.md) these cryptographic operations can be generally applied to different blockchain and even to different pubblication media. However, the outstanding properties of Bitcoin consensus algorithm in particular related to decentralization, censorship resistance and permissionlessness make it the ideal technologycal stak for developing advanced programmability features such as those required by digital bearer rights and smart contracts.

## Single-use Seals in Bitcoin Transactions and RGB

From previously, we recall that Single-use Seals creation undergo two fundamental operations: **Seal Definition** and **Seal Closing**. We will now explore how these two operations can be implemented **using Bitcoin as a pubblication medium**, and in particular making use of some elements of **Bitcoin Transactions**. 

There are 2 main ways in which a Single-use Seal can be **defined** in Bitcoin transactions:

* **Public keys or addresses** - the seal is defined selecting an address or a public key which has not been used yet (i.e. has not been used by any locking script, thus is not locking any bitcoin)
* **Bitcoin transaction outputs** – the seal is defined by selecting a specific UTXO available to some wallet.

This definition methods can be employed in a combination of **closing methods** which differentiate themselves according to how a **spending transaction**:
1. Uses the seal definition: use of the address in locking script / spend of the UTXO.  
2. Host the message over which the seal is closed according to a **commitment scheme** (i.e. in which part of the transaction the message is committed and stored).
     
The following table illustrates the 4 possible combinations of seal definition and seal closing:

| Scheme name  | Seal Definition         | Seal Closing            | Additional Requirements                             |  Main application              | Possible commitment schemes      |
|--------------|-------------------------|-------------------------|-----------------------------------------------------|--------------------------------|----------------------------------|
| PkO          | Public key value        | Transaction output      | P2(W)PKH                                            |  none yet                      | Keytweak, tapret, opret          |                  
| **TxO2**     | **Transaction output**  | **Transaction output**  | **Requires Deterministic Bitcoin Commitments**      |  **RGBv1 (universal)**         | **Keytweak, tapret, opret**      |                  
| PkI          | Public key value        | Transaction input       | Taproot-only - Not working with legacy wallets      |  Bitcoin-based identities      | Sigtweak, witweak                |                  
| TxOI         | Transaction output      | Transaction input       | Taproot-only - Not working with legacy wallets      |  none yet                      | Sigtweak, witweak                | 

**RGB protocol uses the TxO2** scheme in which both seal definition and the seal closing uses trasnsaction outputs (the "**O2**" in **TxO2** acronym stand for **2 Outputs**).

As shown in the table, several **Commitment schemes** can be used for each ** seal closing method**. Each method is differentiated by the location used by the related transactions to host the commitment, and in particular, whether the message is committed in a location belonging to the transaction input or output:
* Transaction Input:
     * Sigtweak - the commitment is placed inside the random 32-byte **r** component constituting the **<r,s>** ECDSA signature pair of an input. It make uses of [Sign-to-contract (S2C)](https://blog.eternitywall.com/2018/04/13/sign-to-contract/#sign-to-contract).
     * Witweak - the commitment is placed inside the segregated witness data of the transaction.
* Transaction Output (ScriptPubKey):
     * Keytweak - It uses the [Pay-to-contract](https://blog.eternitywall.com/2018/04/13/sign-to-contract/#pay-to-contract) construction through which the outpu's public key of the output is "tweaked" (i.e. modified) in order to contain a deterministic reference to the message.   
     * **Opret** - The message committed is placed as an unspendable output after`OP_RETURN` opcode.
     * **Tapret (taptweak)** - This scheme represent a form of tweak in which the message is committed into an `OP_RETURN` tagged string placed into a leaf in the `Script path` of a [taproot transaction](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) which thus change the value of the PubKey.
    
![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/d0bc6d55-0918-48c1-b97d-73071f98874b)


## TxO2 Client-side Validation 

In the next paragraphs we will focus on client side validation combined with single-use seal definition an closing operation of the **TxO2** scheme, showing them step by step below and using the 2 usual cryptographic characters: Alice, dealing with a seal operation, and Bob as an observer.

1. First of all Alice, have some UTXO at her disposal **which reference some client validated data known only by her**.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/ad0684d1-294c-49e7-b80a-3ae6c5156a38)

2. Alice communicate to Bob that the spending of some UTXO represent the signal that something has happened.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/c232438e-8571-492e-828d-d2c5e31760b8)

3. Once Alice spend its UTXO, only Bob knows that this spend has an additional meaning even if everybody (i.e. the audience of Bitcoin Blockchain) can see this event.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f770fd32-e903-49b0-a3ea-d604fd189770)

4. Indeed, the UTXO spent by Alice through the **witness closing transaction** contains a commitment to the client-side validated data. By passing the original data to Bob, she is able to prove to Bob that those data are duly referenced by the commitment placed by Alice in the spending transaction. The verification operation is performed by Bob independenly, using the appropriate methods that are part of the client-side validation protocol (e.g. RGB protocol).  

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f6440aae-202a-4569-bea7-f46664c00e92)

The key point of single-use seal usage in combination with client-side validation consists in the uniqueness of the spending event and the data committed (i.e. the message) to it, which cannot be altered in the future. The whole operation can be summed up in the following terms.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/dd575319-8eb8-48c2-837a-b6b7bf4faa81)

The next important step is to illustrate precisely how the two commitment schemes, **opret** and **tapret** works and which are the features they need to fullfill, in partircular related to determinism of the commitment.   

## Deterministic Bitcoin Commitment - DBC

For RGB commitment operations, the main requirement for a Bitcoin commitment scheme to be valid is that:
> The witness closing transaction must provably contain a single commitment.

With this requirements it is not possible to construct some "alternative story" related to the commitment of the client-side data in the same transaction. This way the message around which we close the single-use seal is unique. In order to fullfill the requirement, independently of the number of outputs in a transaction, *one and only one output* for each commitment scheme (opret and tapret) is valid:

> Uniqueness of the RGB commitment: the only valid outputs which can contain an RGB message commitment are:
> 1. The first OP_RETURN output (if present) for `opret` commitment scheme.
> 2. The first taproot output (if present) for `tapret` commitment scheme.

It is worth noting that a transaction can contain both a single `opret` and a single `tapret` commitment in two distinct outputs. Naturally, those commitments will commit to different client-side validated data that, as we will see later, indicates explicitly the commitment method used to reference themself.   

### Opret

It's the most simple and immediate scheme. The commitment is placed in the first OP_RETURN outputof the witness transaction in the following way:
```
34-byte_Opret_Commitment =
OP_RETURN OP_PUSHBYTE_32 <tH_MPC_ROOT>
|________| |___________| |____________|
  1-byte       1-byte       32 bytes                      
```
`tH_MPC_ROOT` is a 32-byte Tagged Multi Protocol Commitment (MPC) Merkle_Root hash so that the total size of the commitment in the *ScriptPubKey* is 34 bytes.

### Tapret

Tapret scheme contitutes a more complex form of deterministic commitment and represents an improvement in terms of on-chain footprint and privacy of contract operations. The main idea behind this application is to hide the commitment inside the `Script path Spend` of a [taproot transaction](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki). 

First of all, before showing how the commitment it is actually embedded in a taproot transaction, we will show the exact **form of the commitment which is a 64-byte** string [constructed](https://github.com/BP-WG/bp-core/blob/master/dbc/src/tapret/mod.rs#L179-L196) in the following way:
```
64-byte_Tapret_Commitment =

OP_RESERVED ...  ... .. OP_RESERVED  OP_RETURN  OP_PUSHBYTE_33  <tH_MPC_ROOT>  <Nonce>
|__________________________________| |________| |_____________| |____________| |______|
 OP_RESERVED x 29 times = 29 bytes     1 byte       1 byte         32 bytes    1 byte
|_____________________________________________________________| |_____________________|
        TAPRET_SCRIPT_COMMITMENT_PREFIX = 31 bytes               MPC commitment + NONCE = 33 bytes
```
So the 64-byte `tapret` commitment is an `Opret` commitment prepended with 29 bytes of OP_RESERVED operator and to which is appended a 1-byte `Nonce` whose utility will be address [later](#nonce-optimization).   

In order to preserve highest degree of implementation flexibility, privacy and scalability, **Tapret scheme has been designed to integrate many different cases which occurs according to the bitcoin spending need of the user**, in particular we differentiate between the following tapret scenarios:
* **Single incorporation** of RGB Tapret commitment into a taproot transaction **wihout Script Path Spend structure**.
* **Integrate** the Tapret RGB commitment into a taproot transaction containing a **pre-existing Script Path Spend structure**.

We will explore each one of these scenarios below.

#### Tapret Incorporation without Script Path Spend

In order to show this first scenario, below we show the standard a taproot output Key `Q` constituted by just an internal `P` key and **no Script Path Spending**

```
+---+            +---+   +---+   +---+
| Q |      =     | P | + | m | * | G |
+---+            +---+   +-^-+   +---+
                           |
                    +-------------+
                    | tH_TWEAK(P) |
                    +-------------+
```
* `P` is the Internal Public Key of the *Key Path Spend*
* `G` is the Generator point of secp256k1 curve
* `tH_TWEAK(P)` = SHA-256(SHA-256(*TapTweak*) || SHA-256(*TapTweak*) || P)  which makes use of [BIP86](https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki#address-derivation) to demostrate there  is no Script Path Spend

To insert tapret commitment in such a transaction, we modify the transaction in order to provide the commitment as a single script, according to the following scheme:
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

* `P` is the Internal Public Key of the *Key Path Spend*
* `G` is the Generator point of secp256k1 curve
*  `m` is the tweaking hash
* `tH_TAG(x)` = TaggedHash("tag_id",x) = SHA-256(SHA-256(*tag_id*) || SHA-256(*tag_id*) || x)
     * `tH_TWEAK(x)` = SHA-256(SHA-256(*TapTweak*) || SHA-256(*TapTweak*) || x)
     * `tH_BRANCH(x)` = SHA256(SHA-256(*TapBranch*) || SHA-256(*TapBranch*) || x)

The proof of inclusion and uniqueness in the Taproot Script tree is constituted by only the Internal Key `P`. 

#### Tapret incorporation in pre-existing Script Path Spend

To go through the construction of this more complex case we show below the structure of a taproot output Key `Q`, which in this example is constituted by a Key Path Spend with internal key `P` and a 3-script tree in the Script Path Spend.

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

* `tH_TAG(x)` = TaggedHash("tag_id",x) = SHA-256(SHA-256(*tag_id*) || SHA-256(*tag_id*) || x)
     * `tH_LEAF(x)` = SHA-256(SHA-256(*TapLeaf*) || SHA-256(*TapLeaf*) || version_leaf(x) || size(x) || x)
* `A, B, C` are some Bitcoin scripts of this Taproot Tree  

The rule of RGB Tapret commitment imposes the following prescriptions:

1. **The Tapret Commitment is inserted as an unspendable script at the 1st Level of the Script Tree, shifting all other scripts 1 level below.**

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

2. According to Taproot rules, **every hashing operation of branch and leaves is performed in lexicographic order of the two operands**. Thus, two cases can occur, leading to two different proof of uniqueness of the commitment:
     1. If the tapret commitment hash (`tHT`) **is greater** than the upper level hash of the Script Path Spend (`tHABC`), it will be put on **the right  of Script Tree**. In this case, as per RGB protocol rules, the commitment in this position is cosidered as a valid proof of uniqueness and the merkel proof of inclusion and uniqueness of the commitmentis consituted by `tHABC` and `P` only.
     2.  If the tapret commitment hash (`tHT`) **is smaller** than the upper level hash of the Script Path Spend (`tHABC`), it will be put on **the left of the Script Tree**. In this case, it must be demonstrated that on the right side of the Tree there is no other tapret commitment. To do so, `tHAB` and `tHC` need to be disclosed and constitute the merkle proof of inclusione and uniqueness together with `P`.

&nbsp;
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

&nbsp;
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
#### Nonce optimization

As an additional method of optimization the `<Nonce>` which represent the last byte of the `64_byte_Tapret_Commitment` allows for the user contructing the proof to attempt at "mining" a `tHT` such that `tHABC < tHT`, thus placing it in the right side of the tree and definitely avoiding to reveal the constituents of the script branch (in this example `tHaB` and `tHC`) 

## Multi Protocol Commitment - MPC

Multi Protocol commitments address the following important requirement:

1. How the tagged value which is committed according to either `opret` or `tapret` schemes is constructed?
2. How it is possible to store in a single commitment the state change of more than one contract / state transition?     

In practice the previous points are address through an **ordered merkelization** of the multiple contracts / state transitions associated to the UTXO which are being spent by the **witness closing transaction** in which such multiple transitions of eventualy commited by mean of DBCs.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/db6c410c-9ce1-4575-b0b4-e7c09f38d502)

### MPC Tree root

The MPC tree root, which goes either in [opret](#opret) or [tapret](#tapret) commitment is the `tH_MPC_ROOT(x)` constructed in a BIP-341-fashion as follows:

`tH_MPC_ROOT(x) = SHA-256(SHA-256(urn:lnpbp:lnpbp0004:tree:v01#23A) || SHA-256(urn:lnpbp:lnpbp0004:tree:v01#23A) || x)`

### MPC Tree Construction

In order to construct the MPC tree we must **deterministically provide a position of the leaf belonging to each contract**, thus: 

> Setting `C` has the number of contract `c_i` to be included in the MPC we can build a tree with `w` leaves with `w > C` (corresponding to a depth `d` such that `2^d = w`), such that each contract identifier `c_i` representing a different contract is placed at unique position `pos_i = c_i mod w`    

In essence, the construction a suitable tree of width `w` hosting each contract `c_i` in a unique position position represent a sort of mining process. The bigger is the number of contract `C` and the bigger should be the number of leaves `w`. Assuming a random distribution of the `pos_i`, as per [Birthday Paradox](https://en.wikipedia.org/wiki/Birthday_problem), we have ~50% probability that a collision in the position occurs in a tree with `w ~ C^2` ).

In order to avoid too big MPC trees, and beeing the occurence of collision a random process, an additional optimization has been introduced. The modulus operation has been modified as following: pos_i = `c_i + cofactor mod w` where `cofactor` is a 16-byte random number that can be chosen as a "nonce" to get distinct `pos_i` values with `w` being fixed. The tree construction process start from the smallest tree such that `w > C`, then trying a certain number of `cofactor` attempts, if none of them is able to produce `C` distinct positions, `w` is increased and a new series of `cofactor` trials is attempted.

#### Contract Leaves (Inhabited)

Once `C` distinct positions `pos_i` are found the corresponding leaves are populated in the following way:

`tH_MPC_LEAF(c_i) = SHA-256(SHA-256(urn:lnpbp:lnpbp4) || SHA-256(urn:lnpbp:lnpbp4) || c_i || BUNDLE_i )` 

Where:
* `c_i` is the 32-byte contract_id which is the hash of the [genesis]() of the contract itself
* `BUNDLE_i` is the 32-byte hash that is calculated from the data of the bundle of state transition.  

#### Entropy leaves (Uninhabited)

For the remaining `w - C` uninhabited, a value must be committed. In order to do that, each leaf in position `j != pos_i` for every `i = 0,...,C-1` is populated in the following way:

`tH_MPC_LEAF(j) = SHA-256(SHA-256(urn:lnpbp:lnpbp4) || SHA-256(urn:lnpbp:lnpbp4) || entropy || j )

 Where:
 * `entropy` is a 64-byte random value chosen by the user contructing the tree

The followign diagram shows the costruction of a sample MPC tree where: of  and populated by C = 3 contracts, and 
* `d = 3 (w = 8)`
* `tH_MPC_BRANCH(tH1 || tH2) = SHA-256(SHA-256(urn:lnpbp:lnpbp4) || SHA-256(urn:lnpbp:lnpbp4) || d || w || tH1 || tH2)`
*  `d` and `w` is the tree depth and width respectively
*  `pos_1 = 7, pos_2 = 4, pos_3 = 2` 

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
        +------+                   +-----+                   +-----+                   +-----+                   +-----+                   +-----+                   +-----+                    +----+
        |                          |                         |                         |                         |                         |                         |                          | 
+-------+----------+      +--------+---------+      +--------+---------+      +--------+---------+      +--------+---------+      +--------+---------+      +--------+---------+       +--------+---------+ 
|   entropy || 0   |      |   entropy || 1   |      | c_3 || BUNDLE_3  |      |   entropy || 3   |      | c_2 || BUNDLE_2  |      |  entropy || 5    |      |  entropy || 5    |       |  c_1 || BUNDLE_1 | 
+------------------+      +------------------+      +------------------+      +--------+---------+      +--------+---------+      +--------+---------+      +--------+---------+       +--------+---------+


```












 
