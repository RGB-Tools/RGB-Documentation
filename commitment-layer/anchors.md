# Anchors

Anchors are the client-side validated structures that summarizes all the data needed to validate contract commitments, which were described in the previous section. They are composed by the following ordered fields:

* `Txid`&#x20;
* `MPC Proof`&#x20;
* `Extra Transaction Proof ETP`

Where:

## TxId

`Txid` is the 32-byte Bitcoin Transaction Id which contains the data-related to `Opret`  or  `Tapret` commitment. Note that `TxId` could theoretically be reconstructed from the off-chain data of state transitions pointing to each on-chain closing transaction, however for simplicity they are included in the anchor.

## MPC Proof

The `MPC Proof` of the contract `c_i` consists of `pos_i` `cofactor` `Merkle Proof` which were described [previously](multi-protocol-commitments-mpc.md#mpc-tree-construction).

## Extra Transaction Proof - ETP

If an [Opret](deterministic-bitcoin-commitments-dbc/opret.md) commitment is used, no additional proof is provided in this field, since, as described in [the previous section](deterministic-bitcoin-commitments-dbc/opret.md), the verifier inspects the first `OP_RETURN` output finding the correct `mpc::Commitement`.

If a [Tapret](deterministic-bitcoin-commitments-dbc/tapret.md) commitment is used, a so called **Extra Transaction Proof - ETP** must be provided, which consists of:

* Internal Public Key `P` of the Taproot output used.
* Partner node(s) of the [Taproot](../annexes/glossary.md#taproot) `Script Path Spend` which is either:
  * The top left branch (in the [example](deterministic-bitcoin-commitments-dbc/tapret.md#tapret-incorporation-in-pre-existing-script-path-spend): `tHABC`) if the `Tapret` commitment is on the right side of the tree.
  * The left and right nodes of the upper right branch (in the same example they are: `tHAB` and `tHC`) if the `Tapret` commitment is on the left side of the tree.
* The [nonce](deterministic-bitcoin-commitments-dbc/tapret.md#nonce-optimization), if used, to optimize the Partner node part of the proof.

In the next section we will introduce concepts purely concerning the off-chain part of RGB, i.e., contracts, giving an abstract view of the partially replicated finite state machine that gives RGB a much greater expressiveness than can be achieved through Bitcoin Script without sacrificing confidentiality

***
