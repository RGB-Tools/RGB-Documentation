# Opret

This represents the simplest and most straightforward scheme. The commitment is inserted into the first `OP_RETURN` output of the [witness transaction](../../annexes/glossary.md#witness-transaction) in the following way:

```
34-byte_Opret_Commitment =
 OP_RETURN   OP_PUSHBYTE_32   <mpc::Commitment>
|_________| |______________| |_________________|
  1-byte       1-byte         32 bytes                      
```

`mpc::Commitment` is the 32-byte Tagged hash resulting from the [MPC tree](../multi-protocol-commitments-mpc.md#mpc-tagged-hash) which is covered in detail [later](../multi-protocol-commitments-mpc.md). Hence an opret commitment will have a total size of 34 bytes.

***
