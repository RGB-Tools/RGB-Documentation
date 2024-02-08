# Design goals

RGB is a suite of protocols for scalable & confidential smart contracts for Bitcoin & Lightning Network. It embraces the concepts of private & mutual ownership, abstraction and separation of concerns and represents "post-blockchain", Turing-complete form of trustless distributed computing which does not require introduction of "tokens".

The smart contract system proposed in this work is designed according to the following criteria:

**Scalability**, achieved at multiple layers: ability to scale in terms of data size due to client-side-validations; ability to scale in terms of transaction throughput due to lightning network compatibility.

**Strong ownership:** smart contract operates "owned state" which have a well-defined owner(s). Nobody except this owner(s) can update the state of the contract. Contracts always define types of rights as a set of operations which may be performed over the contract and these rights are assigned to be either "public" or "owned", utilizing right-specific validation logic.

**Confidentiality:** data should be known only to contract participants, namely state owners, unless they decide to make them public (disclose). All parts of the protocol must be protected from tools like chain analysis and the protocol should not store any information in the public ledgers.

**Separation of concerns:** the protocols must be designed in a modular and layered way, where each module solves one and only one task. The layers must be well abstracted, meaning that the layers below must be unaware of the structure of the layers above. Such separation of concerns provides a foundation for the protocol interoperability, security, composability and forward-compatibility.

**Extensibility:** it must be possible to create advanced forms of smart contracts without the need to change the core of the protocol or add code & recompile RGB libraries.

**Determinism:** the RGB validation logic must be deterministic in a sense that giving the provided set of inputs and the state of commitment layer (blockchain or lightning channel) it always produces the same result independently of the used platform or linked libraries. This is achieved by two main components: (1) the core of the validation logic generic to all contracts is implemented in rust language and must be used from any system running RGB using language bindings, (2) all contract-specific validation logic runs on [AluVM](https://github.com/internet2-org/aluvm-spec) – a highly deterministic functional virtual machine providing platform-independent instruction set.

**LNP/BP interoperability:** RGB must work well with all existing bitcoin and lightning technologies and be compatible with possible future upgrades.
