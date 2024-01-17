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
This kind of philosophy is at the core of RGB architecture, as the bearer rights of each rightful party is contained in the contract itself and can be modified and enforced digitally, following the rule of the contract itself. 

In RGB design a wider range of issues regarding programmability of smart contract have been taken into account, in particular:
1. A contract may be associated to a *digital asset*, but it's not limited to it. A wider range of applications and extensions of the *smart contract* concept can be implemented in RGB. 
2. Differently from other public blockchain's approach to smart contracts, in RGB there is a clear separation among the different parties related to a contract: e.g. the creator of the contract and the different kind of users interacting in some ways with it. This include in particular the differentiation between:
    * the possibility to *observe* some properties or operations performed by other parties over the contract
    * the possibility to *perform a set of operations* permitted by the contract

**No other counterpart can interact or even observe** the operation performed on the contract, if not allowed by the authorized parties. Inside RGB this characteristics means that there is always an **owner** which is a party which possesses the right to perform some operation on the contract, which are defined by the contract itself.

In order to achieve this goals, a RGB contract is composed by 2 main components:
* State
* Business Logic (Behavior) 

In fact the Business Logic of the contract represent the rules that allows to the entitled party (the owner) to change the state of the contract.

![Alt text](img/state-business-logic.png)


## State 

The state represent a set of conditions which are expressed by the contract itself.
This sets of conditions, in reality, are a **set of arbitrary rich data** which:
* are strongly typed, which means that each variable possesses a clear type definition (e.g. u8) and both lower and upped bounds.
* can be nested, meaning that a type can be constructed from other types 
* can be organized in `lists` `sets` or `maps`

An additional element is that the state are constructed in order to be **atomic** so that their **ownership** and possibility of modification represents a well defined operation.









