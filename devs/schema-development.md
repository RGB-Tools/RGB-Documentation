# Schema development

Schema developer workflow:

1. Select existing RGB schema standards, strict encoding type libraries and embedded verification procedures or AluVM libraries.
2. Write necessary type system in Strict (type language for defining data types and their serialization).
3. Write necessary validation logic using either rust in RGB Core (availablie only temporarily), or AluVM with assembly language or forthcoming ParselTongue
4. Write a new schema (root schema and subschemata) in Contractum languague, using imported interfaces from RGB schema standard library, Strict type system libraries (including the ones created in pt.2) and validation procedures from pt.2.
5. Compile the schema and other newly created libraries into binary forms, which will provide both binaries and symbol files (used in debugging and package distributions for wallet/exchange developers) for RGB, strict encoding and AluVM.
6. Prepare a manifest file, which will contain information about the developer, necessary certificates and information for creating a package containing all required schema information and libraries, which can be distributed to the wallet, exchange developers and contract issuers (via Bifrost or by other means).
7. Run RGB packaging tool to sign all libraries and pack them into the package, uploaded to the Storm network and other centralized package managers.
