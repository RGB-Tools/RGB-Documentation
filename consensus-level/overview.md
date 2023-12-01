# Overview

RGB contracts are bearer agreements which are being maintained independently of each other.

Each user has a partial view on the contract state.

Contract state forms: owned and global

Types of contract state. Data type system. Formal verifiability.

Definition of a contract. Interfaces, Schemata, Genesis.

State transitions.

State extensions (“decentralized genesis”). The way they work.

_RGB smart contract_ defines _state_, _owners_ of that state, and _operations_, which participants of the contract (owners and sometimes more broad public) can execute to update the state.

_Operations_ include _genesis_ operation (_issuance of the contract_), _state transitions_ updating the existing state (or adding to the state data) and _state extension_, which represent a mechanism how anybody (public) can participate in the contract operations.

_State_ of the contract consists of _state atoms_ of different _data types_. _Data types_ are defined in the same terms as variable types in any structural language (C, Rust, Haskell, etc).

RGB contract always have a well-defined parties of the contract, which hold _ownership rights_ over _atoms of state_. The state owned by a contract party is called _owned state_.

Let's start with writing a simple contract managing decentralized identity backed by a PGP key. The "smartness" of the contract (comparing to normal PGP/GPG and Web of Trust) comes from the fact that when a revocation operation is executed, everybody in the world will know about it (since they can see that the UTXO, associated with the key -- the owned state -- was spent), and it can be proven whether at any given moment of time the identity was valid -- or it was already revoked.

5.5. Availability of the global state
