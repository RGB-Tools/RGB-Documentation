# Contract Issuance Workflow

##

In a previous section it was stated that by virtue of its characteristic of being a blueprint for contracts on RGB a Schema will be written by someone and will be used later by someone else not necessarily capable of programming. The workflow for writing a Schema is as follows:

1. Selection of existing standard Schema on RGB, libraries for strict encoding types and built-in verification procedures or AluVM libraries.
2. Writing the type system in Strict (type language for defining data types and their serialization).
3. Write the necessary validation logic using either Rust in RGB Core, or AluVM with assembly language or ParselTongue (under development).
4. Write a new Schema (root Schema and subschemata) in the _**Contractum**_ language, using interfaces imported from the standard RGB schema library, Strict type system libraries (including those created in p. 2), and the validation procedure from p. 2.
5. Compile the Schema and other libraries created from scratch in binary format, which will provide binaries and symbol files for RGB (used in debugging and package distribution for wallet/exchange developers), strict encoding, and AluVM.
6. Prepare a manifest file that will contain developer information, necessary certificates, and information to create a package containing all the required Schema information and libraries that can be distributed to the wallet, exchange developers, and smart contract issuers (via Bifrost or other means).
7. Run the RGB packaging tool to sign all libraries and place them in the package, upload them to the Storm network and other centralized package managers.
