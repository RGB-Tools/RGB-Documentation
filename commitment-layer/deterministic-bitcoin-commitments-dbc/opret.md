# Opret

This is the simplest and most straightforward scheme. The commitment is inserted into the first output `OP_RETURN` of the witness transaction in the following way:

```
34-byte_Opret_Commitment =
OP_RETURN OP_PUSHBYTE_32 <mpc::Commitment>
|________| |___________| |________________|
  1-byte       1-byte         32 bytes                      
```

`mpc::Commitment` is the 32-byte Tagged hash resulting from the [MPC tree](../multi-protocol-commitments-mpc.md#mpc-tagged-hash)  , so that the total commitment size in the _ScriptPubKey_ is 34 bytes.
