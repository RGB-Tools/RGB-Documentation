# Deterministic Bitcoin Commitments - DBC

For RGB commitment operations, the main requirement for a Bitcoin commitment scheme to be valid is that:

> The witness transaction must provably contain a single commitment.

With this requirement, it is not possible to construct an "alternative history" related to client-side data commitment in the same transaction. Thus, the message around which the single-use seal is closed is unique. To meet the above requirement, regardless of the number of outputs in a transaction, _one and only one output_ is valid for each commitment scheme (opret and tapret):

> The only valid outputs that can contain an RGB message commitment are:
>
> 1. The first output OP\_RETURN (if present) for the `Opret` commitment scheme.
> 2. The first taproot output (if present) for the `Tapret` commitment scheme.

It is worth observing that a transaction **can contain both a single** `Opret` **and a single** `Tapret` commitment in two separate outputs. Of course, these commitments will commit to different client-side validated data which, as we shall see later, explicitly indicate the commitment method used to refer to themselves.
