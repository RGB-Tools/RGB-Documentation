# RGB invoices

This section explores how invoices are structured and function within a particular system. The initial focus is on RGB identifiers, which are integral to the operation of the system and have likely been encountered by users in various forms. These identifiers are unique to each component of the system, including contracts, assets, and interfaces, ensuring a standardized method of identification throughout the system.

## Identifiers and Their Encoding

Each element within the system, be it a contract, schema, interface, interface or asset is assigned a unique identifier. These identifiers are not arbitrary strings but are carefully encoded using base 58, a method chosen for its efficiency and readability. Furthermore, these identifiers are prefixed with a descriptor (in the form of a URL or URN) indicating their type, such as "RGB:" for contracts or "RGB:" plus other things for interfaces. This prefixing strategy ensures clarity regarding the nature of each identifier, preventing confusion and misuse.

## Enhancing Human Readability through Chunking

The concept of chunking is introduced as a means to enhance the readability and verifiability of these identifiers. This technique, commonly used in phone and credit card numbers, breaks down long strings into smaller, more manageable segments. This not only aids in human parsing but also in verification processes, where checking the integrity of an identifier involves examining specific segments, such as the checksum at the end. Chunking thereby offers a balance between security and usability, with each chunk providing a certain level of security assurance. For example, having 256-bit strings divided into six blocks means that each chunk adds about 256/6 (~42) bits of security.

Initially, bech 32 coding was considered for use in the system. Despite the potential for shorter QR codes and error correction capabilities, base 32 proved to be more time-consuming and less practical than base 58, especially in terms of readability and QR code size: it is not recommended for use for strings longer than 90 characters. Similar discourse for bech32m. The decision to return to base 58, the format originally used by Bitcoin, was dictated by these results and the realization that error correction was not as crucial as previously thought, given the system's verification mechanisms.

## Utilizing URLs for Enhanced Interaction

A significant advantage of the chosen identifier system is its compatibility with URLs, allowing for direct interaction with wallets through simple clicks. This contrasts sharply with the cumbersome process required by other systems, where multiple steps are needed to copy and paste identifiers into wallets. The URL format's simplicity and efficiency in opening wallets and facilitating transactions underscore its superiority over alternatives.

## Invoice Structure and Alternatives

The structure of invoices within this system is detailed, highlighting how they incorporate chunked contract IDs and interface names to specify payment details clearly. Alternatives to the direct use of contract IDs, such as using asset tickers or mnemonic checksums, were considered but ultimately rejected due to security concerns and the potential for confusion. The chosen format prioritizes clarity and security, ensuring that users can easily understand and verify the details of their transactions.

## The Command Line Interface and Workflow

RGB includes an all-in-one tool that allows you to work with these URLs through the command-line interface, for example, to verify and process invoices. Including invoice generation, transaction construction and verification, and seamless integration of RGB assets into the transaction process. The workflow demonstrates the efficiency and security of the system, highlighting its potential to simplify and secure transactions in a variety of contexts.

In conclusion, the system's approach to invoices, identifiers, and transactions is meticulously designed to balance security, usability, and efficiency. Through the use of unique identifiers, chunking, and strategic choice of encoding methods, it provides a robust framework for managing and verifying transactions with ease and accuracy.