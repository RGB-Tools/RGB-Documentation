# Client-side Validation with Bitcoin

In this section we will explore the application of client-side validation and single-use seal to Bitcoin Blockchain, introducing the main architectural features behind **RGB** protocol.
As mentioned in the [previous chapter](intro-tech.md) this cryptographic operations  

Basically, there are 2 ways in which a Single-use Seal can be defined and subsequently close on bitcoin:

* Public key or address – the seal is closed when the first use of it take place. The committment to client-side validated data is accomplished with the signature of the inputs.
* Bitcoin transaction output – the seal is closed by spending an UTXO selected in the seal definition. The commitment to the client-side validated data can be done in several ways inside the spending transaction.

In the following table we summarize the scheme that can be employed:

| Scheme name  | Seal Definition   | Seal Closing   | Additional Requirements   |  Main application  |Possible commitment schemes  |
|--------------|-------------------|----------------|---------------------------|--------------------|-----------------------------|
|   |   |   |   |   |   |                                    |
|   |   |   |   |   |   |                                    |
|   |   |   |   |   |   |                                    |



 
