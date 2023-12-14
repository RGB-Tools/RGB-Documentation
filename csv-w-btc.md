# Client-side Validation with Bitcoin

In this section we will explore the application of client-side validation and single-use seal to Bitcoin Blockchain, introducing the main architectural features behind **RGB** protocol.
As mentioned in the [previous chapter](intro-tech.md) this cryptographic operations  

Basically, there are 2 ways in which a Single-use Seal can be defined and subsequntly close on bitcoin:

* Public key or address – we close it with its first use. The committment to new data is accomplished with the signature of the inputs.
* Bitcoin transaction output – we close it by spending the UTXO. There are many ways to commit to the new data. 
