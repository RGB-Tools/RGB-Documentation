# Introduction to schema and interfaces

An RGB _Schema_ is the reification of a standard/blueprint for the construction of an RGB smart contract. It can be viewed as the analogue of a class for an OOP language or the RGB analogue of an ERC standard for Ethereum contracts. So, a Schema defines a standard for RGB assets, for example: fungible assets, collectibles, digital identities etc...

The issuer of a token on RGB uses a Schema to define the issuing contract so that it is supported by wallets and exchanges. So, when wallets and exchanges collect information regarding some asset on RGB (data and contract) they need to validate it against the Schema used by the issuer of that asset. Only if the Schema validation is successful, i.e., does not fail, then the contract state transition requested by the user can be made.

## Internal mechanics of a Schema

From a technical point of view, a Schema defines the requirements needed to validate state transitions outside the authorization level (state owned) provided by Bitcoin Script-managed commitments. It also allows for simple updates to the contract without having to modify the software, so that wallets, explorers, and LN nodes can accept new asset types without making any changes to the code. The Schema is, therefore, the set of validation rules for the client-side part of RGB. The schema may contain Turing-complete scripts that define the business logic for client-side validation. The various objects defined in the script schema are used during validation of state transitions on _AluVM_.

In RGB the Schema is always defined by the issuer in the genesis state. In it, the following are defined descriptively/functionally:
- the _types_ for 
  - metadata (and restrictions on their values);
  - owned state;
  - global state;
  - valences (public rights);
  - possible combinations of the above via state transitions.
- State validation functions (executed by AluVM), i.e., functions that have type-signatures of the type `validate :: state -> bool`, for each data type and operation.

Thus, a Schema functionally answers the following questions:

- What kinds of owned states and assignments exist?
- What kinds of valences (publicly-executable rights) exist?
- What global state does the contract have?
- How is the genesis contract structured?
- What state transitions and extensions are possible?
- What metadata can contract operations have?
- How is state data allowed to change with state transitions?
- What sequences of transitions are allowed?

The schema differentiates contract developers from issuers, who know nothing about coding and programming.

A schema allows the creation of "template contracts" while avoiding common mistakes for issuers.

An RGB contract template defines:
- what types of states can exist;
- the types of data used in the state;
- what operations can be performed with the contract;
- the scripts and validation rules (as, for example, *the algebraic sum of the values of the outputs must equal the algebraic sum of the inputs*).

In summary:
```
RGB Schema <- State data Types + Operation types + Graph evolution rules + Used strict type libs + AluVM validation code
```

Recall from the previous chapter that the operations of a smart contract can be divided into state generation and state transition events under a single contract grouped together by a specific finality proof (anchor). More specifically we have:
- State generation:
	- genesis;
	- state extension.
- State transition.
  
Within a contract the state is structured into:
- ***metadata*** ("local" state of the transaction);
- ***assignment***, which consist of.
	- types of property rights (from the schema);
	- definition of the Single-Use-Seal owning that right;
	- state data (optional).
- ***assignments***: public rights (from the schema) without state. Anchor points for _state extensions_.

We can summarize the above in tabular form:

|                    | Genesis | State Extension | State Transition |
|        ----        |   :--:  |      :--:       |       :--:       |
| Metadata           |    +    |       +         |        +         |
| Valences           |    +    |       +         |        +         |
| Assignments        |    +    |       +         |        +         |
| Input              |    No   |       No        |        +         |
| Redeemed Valences  |    No   |       +         |        No        |

## Schema workflow

In the previous section it was stated that by virtue of its characteristic of being a blueprint for contracts on RGB a Schema will be written by someone and will be used later by someone else not necessarily capable of programming. The workflow for writing a Schema is as follows:
1. Selection of existing standard Schema on RGB, libraries for strict encoding types and built-in verification procedures or AluVM libraries.
2. Writing the type system in Strict (type language for defining data types and their serialization).
3. Write the necessary validation logic using either Rust in RGB Core, or AluVM with assembly language or ParselTongue (under development).
4. Write a new Schema (root Schema and subschemata) in the ***Contractum*** language, using interfaces imported from the standard RGB schema library, Strict type system libraries (including those created in p. 2), and the validation procedure from p. 2.
5. Compile the Schema and other libraries created from scratch in binary format, which will provide binaries and symbol files for RGB (used in debugging and package distribution for wallet/exchange developers), strict encoding, and AluVM.
6. Prepare a manifest file that will contain developer information, necessary certificates, and information to create a package containing all the required Schema information and libraries that can be distributed to the wallet, exchange developers, and smart contract issuers (via Bifrost or other means).
7. Run the RGB packaging tool to sign all libraries and place them in the package, upload them to the Storm network and other centralized package managers.