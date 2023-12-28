# Client-side Validation with Bitcoin

In this section we will explore the application of client-side validation and single-use seal to Bitcoin Blockchain, introducing the main architectural features behind **RGB** protocol.
As mentioned in the [previous chapter](intro-tech.md) this cryptographic operations can be generally applied to different blockchain and even to different pubblication media. However, the outstanding properties of Bitcoin consensus algorithm in particular related to decentralization, censorship resistance and permissionlessness make it the ideal technologycal stak for developing advanced programmability features such as those required by digital bearer rights and smart contracts.

## Single-use Seals in Bitcoin Transactions and RGB

From previously, we recall that Single-use Seals creation undergo two fundamental operations: **Seal Definition** and **Seal Closing**. We will now explore how these two operations can be implemented **using Bitcoin as a pubblication medium**, and in particular making use of some elements of **Bitcoin Transactions**. 

There are 2 main ways in which a Single-use Seal can be **defined** in Bitcoin transactions:

* **Public keys or addresses** - the seal is defined selecting an address or a public key which has not been used yet (i.e. have not been used to lock some bitcoins)
* **Bitcoin transaction outputs** – the seal is defined by selecting a specific UTXO available to some wallet.

This definition methods can be employed in a combination of **closing methods** which differentiate themselves according to how a **spending transaction**:
1. Uses the seal definition: use of the address in locking script / spend of the UTXO  
2. Host the message over which the seal is closed according to a **commitment scheme** (i.e. in which part of the transaction the message is committed and stored).
     
The following table illustrates the 4 possible combinations of seal definition and seal closing:

| Scheme name  | Seal Definition         | Seal Closing            | Additional Requirements                             |  Main application              | Possible commitment schemes      |
|--------------|-------------------------|-------------------------|-----------------------------------------------------|--------------------------------|----------------------------------|
| PkO          | Public key value        | Transaction output      | P2(W)PKH                                            |  none yet                      | Keytweak, tapret, opret          |                  
| **TxO2**     | **Transaction output**  | **Transaction output**  | **Requires Deterministic Bitcoin Commitments**      |  **RGBv1 (universal)**         | **Keytweak, tapret, opret**      |                  
| PkI          | Public key value        | Transaction input       | Taproot-only - Not working with legacy wallets      |  Bitcoin-based identities      | Sigtweak, witweak                |                  
| TxOI         | Transaction output      | Transaction input       | Taproot-only - Not working with legacy wallets      |  none yet                      | Sigtweak, witweak                | 


As shown in the table, the possible **commitment schemes** are associated with the places of the transaction in which the messagge is committed which is further differentiate whether the message is committed in transaction input or output:
* Transaction Input:
     * Sigtweak - the commitment is placed inside the random 32-byte **r** component constituting the **<r,s>** ECDSA signature pair of an input. It make uses of [Sign-to-contract (S2C)](https://blog.eternitywall.com/2018/04/13/sign-to-contract/#sign-to-contract)
     * Witweak - the commitment is placed inside the segregated witness data of the transaction
* Transaction Output:
     * Keytweak - It uses the [Pay-to-contract](https://blog.eternitywall.com/2018/04/13/sign-to-contract/#pay-to-contract) construction through which the public key of the output is "tweaked" (i.e. modified) in order to contain a deterministic reference to the message.   
     * **Tapret (taptweak)** - This scheme represent a form of tweak in which the message is committed into a leaf in the `Script path` of a [taproot transaction](https://github.com/bitcoin/bips/blob/master/bip-0341.mediawiki) 
     * **Opret** - It is the most simple commitment scheme, in which the message committed is placed as an unspendable output after`OP_RETURN` opcode.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/d0bc6d55-0918-48c1-b97d-73071f98874b)

         

**RGB protocol uses the TxO2** scheme in which both seal definition and the seal closing uses the Outputs (the "**O2**" in **TxO2** acronym stand for **2 Outputs** meaning that both the seal definition and the seal closing uses transaction Outputs). In particular, the protocol makes use of **tapret and opret** commitment schemes which we will be  in the next section. 


We will focus on this important operation step by step below, using the 2 usual cryptographic characters: Alice, dealing with a seal operation, and Bob as an observer.

1. First of all Alice, have some UTXO at her disposal **which reference some client validated data known only by her**.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/ad0684d1-294c-49e7-b80a-3ae6c5156a38)

2. Alice communicate to Bob that the spending of some UTXO represent the signal that something has happened.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/c232438e-8571-492e-828d-d2c5e31760b8)

3. Once Alice spend its UTXO,  only Bob knows that this spend has an additional meaning even if everybody (i.e. the audience of Bitcoin Blockchain) can see this event.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f770fd32-e903-49b0-a3ea-d604fd189770)

4. Indeed, the UTXO spent by Alice through the **witness transaction** contains a commitment to the client-side validated data. By passing the original data to Bob, she is able to prove to Bob that those data are duly referenced by the commitment placed by Alice in the spending transaction. The verification operation is performed by Bob independenly, using the appropriate methods that are part of the client-side validation protocol (e.g. RGB protocol).  

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/f6440aae-202a-4569-bea7-f46664c00e92)

The key point of single-use seal usage in combination with client-side validation consists in the uniqueness of the spending event and the data committed (i.e. the message) to it, which cannot be altered in the future. The whole operation can be summed up in the following terms.

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/dd575319-8eb8-48c2-837a-b6b7bf4faa81)

The next important step, which we will focus in the next section, is represented by the different methods that allows to store the commitment to the client-side validated data inside Bitcoin trasnactions.   

## Deterministic Bitcoin Commitment 

 
