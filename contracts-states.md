# RGB Contracts and States

## Introduction to Contracts

Finally, after exploring the mechanisms behind the storage of [client-side validated](#csw-w-btc.md) fingerprints into the Bitcoin Blockchain, we can now approach more in depth what kind of data undergoes the hashing and merkelization process just described. Such data are those pertaining to one or more **smart contracts**.  

First of all, what is actually a (smart) contract? 

> A smart contract is an agreement which is automatically enforced between parties

This means that the enforcement of the conditions agreed between the parties **does not require human intervention** and that such enforcement is done by mathematics and computing means. 

In addition to that, a question arises. In order to achieve the highest degree of automatization, decentralization and privacy it is possible to forfeit centralized registry storing contract ownership and information?
The affirmative answer lie back at the origins.
 
 ![Alt text](img/orenoque-contract.png)

 Once upon a time contracts, for examples those of securities, where **bearer instruments**. Indeed, the generalized use of assets ledgers which in fact imply a custody relation with some institution controlling both the ledger and storing the contract on behalf of the client represents a quite recent development of economic history. The bearer nature of contracts is in fact a centuries-old tradition.   
This kind of philosophy is at the core of RGB architecture, as the rights of each rightful party is contained in the contract itself and can be modified and enforced digitally, following the contract itself. 

In RGB design a wider range of issues regarding programmability of smart contract have been taken into account, in particular:
1. A contract may be associated to a *digital asset*, but it's not limited to it. A wider range of applications and extensions of the *smart contract* concept can be implemented in RGB. 
2. Differently from other public blockchain's approach to smart contracts, in RGB there is a clear separation among the different parties related to a contract: e.g. the creator of the contract and the different kind of users interacting in some ways with it. This include in particular the differentiation between:
    * the possibility to *observe* some properties or operations performed by other parties over the contract
    * the possibility to *perform a set of operations* permitted by the contract

