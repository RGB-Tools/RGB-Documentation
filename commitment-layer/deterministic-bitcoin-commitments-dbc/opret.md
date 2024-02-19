# Opret

This is the simplest and most straightforward scheme. The commitment is inserted into the first output OP\_RETURN of the witness transaction in the following way:

```
34-byte_Opret_Commitment =
OP_RETURN OP_PUSHBYTE_32 <tH_MPC_ROOT>
|________| |___________| |____________|
  1-byte       1-byte       32 bytes                      
```

`tH_MPC_ROOT` is a 32-byte Tagged Multi Protocol Commitment (MPC) Merkle\_Root hash, so that the total commitment size in the _ScriptPubKey_ is 34 bytes.
