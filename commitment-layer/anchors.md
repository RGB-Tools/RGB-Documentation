# Anchors

Anchors are the client-side validated structures that summarizes all the data needed to validate contract commitments, which were described in the previous section. They are composed by the following ordered fields:

* `Txid`&#x20;
* `MPC Proof`&#x20;
* `Extra Transaction Proof ETP`

Where:

## TxId

`Txid` is the 32-byte Bitcoin Transaction Id which contains the data-related `opret` `tapret` commitment. Note that `TxId` could theoretically be reconstructed from the off-chain data of state transitions pointing to each on-chain closing transaction, however for simplicity they are included in the anchor.

## MPC Proof

The `MPC Proof` of the contract `c_i` consists of `pos_i` `cofactor` `Merkle Proof` which were described previously.

## Extra Transaction Proof - ETP

If an [Opret](deterministic-bitcoin-commitments-dbc/opret.md) commitment is used, no additional proof is provided in this field, since, as described above, the verifier inspects the first `OP_RETURN` output finding the correct `mpc::Commitement`.

If a [Tapret](deterministic-bitcoin-commitments-dbc/tapret.md) commitment is used, a so called **Extra Transaction Proof - ETP** must be provided, which consists of:

* Internal Public Key `P` of the Taproot output used.
* Partner node(s) of the `Taproot Script Path Spend` which is either:
  * The top left branch (in the [example](deterministic-bitcoin-commitments-dbc/tapret.md#tapret-incorporation-in-pre-existing-script-path-spend) `tHABC`) if the `tapret` commitment is on the right side of the tree.
  * The left and right nodes of the upper right branch (in the example `tHAB` and `tHC`) if the `tapret` commitment is on the left side of the tree.
* The [nonce](deterministic-bitcoin-commitments-dbc/tapret.md#nonce-optimization), if used, to optimize the Partner node part of the proof.

#### Library for Client-side Validation and Deterministic Bitcoin Commitments

Repository:

* https://github.com/LNP-BP/client\_side\_validation

Rust Crates:

* https://crates.io/crates/rgb-core
* https://crates.io/crates/client\_side\_validation
* https://crates.io/crates/bp-dbc

In the next section we will introduce concepts purely concerning the off-chain part of RGB, i.e., contracts, giving an abstract view of the partially replicated finite state machine that gives RGB a much greater expressiveness than can be achieved through Bitcoin Script without sacrificing confidentiality
