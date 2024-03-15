# RGB Protocol Documentation

RGB is a protocol developed in order to enforce digital rights in form of contracts and assets in a scalable and private manner leveraging Bitcoin consensus rules and operations.

This guide targets the broader technical audience willing to understand in depth the RGB protocol, from its theoretical foundations rooted in [Client-side Validation](annexes/glossary.md#client-side-validation) and [Single-use Seals](annexes/glossary.md#single-use-seal) to the more core features of [State Transitions](annexes/glossary.md#state-transition) and Contract Structure. The relevant terms and concepts will be introduced step by step and they will be referenced to external material in case more detailed study by non computer science audience is needed.

## Table of Contents&#x20;

* [Paradigms of Distributed Computing](distributed-computing-concepts/paradigms-of-distributed-computing.md)
* [Client-side Validation](distributed-computing-concepts/client-side-validation.md)
* [Single-use Seals and Proof of Publication](distributed-computing-concepts/single-use-seals.md)

### Commitment Layer

* [Commitment Schemes within Bitcoin and RGB](commitment-layer/commitment-schemes.md)
* [Deterministic Bitcoin Commitments - DBC](commitment-layer/deterministic-bitcoin-commitments-dbc/)
  * [Opret](commitment-layer/deterministic-bitcoin-commitments-dbc/opret.md)
  * [Tapret](commitment-layer/deterministic-bitcoin-commitments-dbc/tapret.md)
* [Multi Protocol Commitments - MPC](commitment-layer/multi-protocol-commitments-mpc.md)
* [Anchors](commitment-layer/anchors.md)

### RGB State and Operations

* [Introduction to Smart Contracts and their States](rgb-state-and-operations/intro-smart-contract-states.md)
* [Contract Operations](rgb-state-and-operations/state-transitions.md)
* [Components of a Contract Operation](rgb-state-and-operations/components-of-a-contract-operation.md)
* [Features of RGB State](rgb-state-and-operations/features-of-rgb-state.md)

### RGB Contract Implementation

* [Contract Implementation in RGB](rgb-contract-implementation/schema-interface.md)
* [Schema](rgb-contract-implementation/schema/)
  * [Non Inflatable Fungible Asset Schema](rgb-contract-implementation/schema/non-inflatable-fungible-asset-schema.md)
* [Interface](rgb-contract-implementation/interface/)
  * [Standard Interfaces by LNP/BP Association](rgb-contract-implementation/interface/standard-interfaces-by-lnp-bp-association.md)
  * [RGB20 Interface example](rgb-contract-implementation/interface/rgb20-interface-example.md)
* [Interface Implementation](rgb-contract-implementation/interface-implementation.md)

### Annexes

* [Glossary](annexes/glossary.md)
* [Contract Transfers](annexes/contract-transfers.md)
* [Invoices](annexes/invoices.md)
* [RGB Library Map](annexes/rgb-library-map.md)

## Credits

The material provided by this guide is based on a 3-days full-immersion seminar on RGB protocol held by [Maxim Orlovsky](https://twitter.com/dr_orlovsky) in Viareggio during the 2nd week of October 2023.&#x20;

Videos:

* [https://planb.network/en/courses/rgb/1/1](https://planb.network/en/courses/rgb/1/1)



