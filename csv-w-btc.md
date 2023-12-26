# Client-side Validation with Bitcoin

In this section we will explore the application of client-side validation and single-use seal to Bitcoin Blockchain, introducing the main architectural features behind **RGB** protocol.
As mentioned in the [previous chapter](intro-tech.md) this cryptographic operations can be generally applied to different blockchain and even to different pubblication medium. However, the outstanding properties of Bitcoin consensus algorithm in particular related to decentralization, censorship resistance and permissionlessness make it the ideal technologycal stak for developing advanced programmability features such as those required by digital bearer rights and smart contracts.       

Basically, there are 2 ways in which a Single-use Seal can be defined and closed using some parts of the Bitcoin transactions:

* **Public keys or addresses**, the seal is closed when the first use of previously selected address/public key takes place (i.e. some funds are locked by a script involving it). The committment to client-side validated data is accomplished with the signature of the inputs.
* **Bitcoin transaction outputs** – the seal is closed by spending an UTXO previously selected in the seal definition. The commitment to the client-side validated data can be done in several ways inside the spending transaction.

It's worth noting that the seal definition method can be different from the seal closing method, such that there 4 combination of methods are available: 



| Scheme name  | Seal Definition         | Seal Closing            | Additional Requirements                             |  Main application              | Possible commitment schemes      |
|--------------|-------------------------|-------------------------|-----------------------------------------------------|--------------------------------|----------------------------------|
| PkO          | Public key value        | Transaction output      | P2(W)PKH                                            |  none yet                      | Keytweak, tapret, opret          |                  
| **TxO2**     | **Transaction output**  | **Transaction output**  | **Requires Deterministic Bitcoin Commitments**      |  **RGBv1 (universal)**         | **Keytweak, tapret, opret**      |                  
| PkI          | Public key value        | Transaction input       | Taproot-only - Not working with legacy wallets      |  Bitcoin-based identities      | Sigtweak, witweak                |                  
| TxO1I        | Transaction output      | Transaction input       | Taproot-only - Not working with legacy wallets      |  none yet                      | Sigtweak, witweak                | 


In particular RGB protocol uses the **TxO2** scheme in which both seal definition and the seal closing uses the Outputs of a chain of connected transactions. The "**O2**" in **TxO2** acronym stand for **2 Outputs** meaning that both the seal definition and the seal closing uses transaction Outputs. 
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

 
