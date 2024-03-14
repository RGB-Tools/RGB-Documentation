# Contract Transfers

In this section we will be guided through a step by steps RGB Contract Transfer operation, again with the cooperation of our cryptographic couple: Alice and Bob.

Let consider the case of Bob, who owns a Bitcoin wallet but has not yet started using RGB technology.

1. To begin operating with RGB protocol, **Bob must install an RGB wallet** and add a contract to it. This startup process involves installing the RGB wallet software, which usually, by default, contains no contracts. The RGB wallet software, in addition, require the ability to interact with Bitcoin UTXO through a Bitcoin wallet and a Bitcoin Blockchain node tool (a full node or an [Electrum Server](https://thebitcoinmanual.com/articles/btc-electrum-server/)). These tools are a mandatory requirement because, as we learned [previously](../rgb-state-and-operations/state-transitions.md#state-transitions-and-their-mechanics), [owned states ](glossary.md#owned-state)are defined over Bitcoin UTXO and represent a necessary item for [state transitions](glossary.md#state-transition) implementing transfer of contract in RGB.
2.  Then, Bob has the task of acquiring the **necessary information about the contracts.** These data, in RGB ecosystem, can be sourced through various channels, such as specific websites, e-mails, or Telegram messages etc, following the [contract issuer](glossary.md#contract-participant)'s choice. These data are distributed using a [contract consignment ](glossary.md#consignment)which is data package containing [Genesis](glossary.md#genesis), [Schema](glossary.md#schema), [Interface](glossary.md#interface) and [Interface Implementation](glossary.md#interface-implementation).

    Each of these parts, usually, consists of as little as 200 bytes of data, meaning **a consignment is typically on the order of a few KiBs**. The contract consignment can also be encoded in Base58 format and sent in a format similar to that of a PGP key or as a QR code. These kind of formats In the future will also easily adaptable to censorship-resistant transmission media such as **Nostr**, through the use of relay servers, or over the Lightning Network.

    At this regards, it's useful to point out that the RGB ecosystem fosters innovation and competition among various wallets by allowing the freedom to propose new methods of contract interaction and transfer. This openness to experimentation and the adoption of new technologies, such as decentralized, censorship-resistant networks, promises to further enrich the capabilities offered by RGB.

<figure><img src="../.gitbook/assets/transfers_0.png" alt="Several channels to acquire an RGB contract in the wallet."><figcaption><p><strong>All the various possible channels for acquiring an RGB contract in the form of consignment in a wallet.</strong></p></figcaption></figure>

3. Once a contract is obtained in consignment format, Bob is able to import it in his RGB wallet and validate the data contained herein. The next thing he can do, is to find someone possessing the contract / asset he is interested to receive in his wallet. In our example, Alice possesses the asset in hes wallet. So, similarly to Bitcoin Transaction **they can setup an RGB Transfer.** The mechanism for discovering stakeholders who have owned state in the contract, such as Alice, remains up to the receiving party, just as the process for discovering who can pay in Bitcoin.
4. I**n order to initiate a transition**, Bob must act first. It does so by **issuing an** [invoice](glossary.md#invoice) which call the specific **transfer method** encoded in the [Schema](glossary.md#schema) of the contract and which he will hand over to Alice. **This invoice generation**, which precede the effective asset transfer, guarantee that the invoice contains **all the relevant instruction needed by Alice to make the transfer**, containing in particular Bob's UTXO derived from his Bitcoin wallet encoded in [blinded form](../rgb-state-and-operations/components-of-a-contract-operation.md#revealed-concealed-form). [Invoices](glossary.md#invoice), which are described in more detail in [this chapter](invoices.md), are generated as simple URL strings and can be transmitted by any means in a manner similar to what we said for consignment.&#x20;

<figure><img src="../.gitbook/assets/image.png" alt=""><figcaption><p><strong>The transfer process begins with an invoice prepared by Bob which contains all the information that Alice need to transfer the asset, in particular the Bob's seal definition, encoded as a Blinded UTXO.</strong></p></figcaption></figure>

5. Alice, who has both a Bitcoin wallet and an RGB wallet with a [stash](glossary.md#stash) of client-side validated data, receive the Invoice from Bob. With the information contained in the invoice, Alice is able to prepare:
   * A [witness transaction](glossary.md#witness-transaction), not necessarily signed, which closes the previously defined [single-use seal](glossary.md#single-use-seal) on her UTXO and committing to the state transition transferring the asset to Bob.
   * A [terminal consignment](glossary.md#terminal-consignment-consignment-endpoint) that encapsulates the final state transition and the history of state transitions since Genesis and contained in validated form in her stash.
6. This **terminal transfer consignment**, obviously larger than a contract consignment because of the inclusion of the entire history of the asset, **is then forwarded to Bob**, who validates and integrates it into his stash, even though the related witness transition has not yet been confirmed into the Bitcoin Blockchain.

<figure><img src="../.gitbook/assets/image (3).png" alt=""><figcaption><p><strong>Alice prepares a witness transaction including the information provided both by Bob's invoice and those coming from her RGB and Bitcoin wallet. In addition, through a transfer consignment allows Bob to verify all the asset history as well as the last state transition addressed to him.</strong></p></figcaption></figure>

7. Bob, after verifying the data contained in the transfer consignment handed over by Alice, may optionally sign a so called _payslip_ which confirm to Alice that:

* Bob agrees on the validity of the client-side validated data included in the consignment.
* Bob agrees that the witness transaction shall be published.

Once published, the witness transaction represent the conclusion of the transfer between Alice and Bob.

<figure><img src="../.gitbook/assets/image (2).png" alt=""><figcaption><p><strong>Optionally Bob can sign a payslip which authorizes Alice to broadcast the witness transaction which marks the conclusion of the transfer between Alice and Bob</strong></p></figcaption></figure>

The following diagram shown an example of transfer interaction between the various element of RGB technology stack composed of RGB wallets, RGB nodes and Electrum Server.

```mermaid
sequenceDiagram
    participant UI1 as UI
    participant WC1 as Wallet controller
    participant RGB1 as RGB Node
    participant ES1 as Electrum Server
    participant Payee
    participant Payer
    participant UI2 as UI
    participant WC2 as Wallet controller
    participant RGB2 as RGB Node
    participant ES2 as Electrum Server

    rect rgb(244, 164, 96)
        note right of ES1: Payee's Wallet
        ES1->RGB1: 
        RGB1->WC1: 
        WC1->UI1: 
    end

    Payee->UI1: create invoice
    UI1->WC1: get invoice
    WC1->ES1: get available UTXOs
    ES1->WC1: UTXO list
    WC1->RGB1: get invoice
    RGB1->WC1: invoice
    WC1->UI1: invoice
    UI1->Payee: invoice string/QR
    Payee->Payer: share invoice

    rect rgb(30, 144, 255)
        note right of UI2: Payer's Wallet
        UI2->WC2: 
        WC2->RGB2: 
        RGB2->ES2: 
    end

    Payer->UI2: scan/paste invoice
    UI2->WC2: decode invoice
    WC2->RGB2: parse invoice
    RGB2->WC2: decoded invoice
    WC2->UI2: decoded invoice
    UI2->Payer: confirmation request
    Payer->UI2: payment confirmation
    UI2->WC2: payment confirmation
    WC2->RGB2: get asset TXOs
    RGB2->WC2: asset TXOs list
    WC2->ES2: get UTXOs list
    ES2->WC2: UTXOs list
    WC2->WC2: get asset balance
    WC2->WC2: coin selection
    WC2->WC2: PSBT creation
    WC2->RGB2: PSBT
    RGB2->WC2: PSBT with commitment state transition
    WC2->RGB2: get consignment data
    RGB2->WC2: consignment data
    WC2->WC1: send consignment to payee (with Proxy Server or Storm)
    WC1->RGB1: validate consignment
    RGB1->ES1: check bitcoin txs confirmation status
    ES1->RGB1: bitcoin txs confirmation status
    RGB1->WC1: validation report
    WC1->WC2: ACK that the provided consignment is valid
    WC2->WC2: sign PSBT
    WC2->ES2: broadcast Bitcoin transaction
    WC2->UI2: tx sent confirmation
    UI2->Payer: tx sent confirmation
    ES1->WC1: bitcoin transaction confirmed
    WC1->RGB1: extract outpoints
    RGB1->WC1: blind UTXOs
    WC1->RGB1: blinding secret
    RGB1->RGB1: blinding secret added to stash
    RGB1->WC1: asset balance update
    WC1->UI1: payment received
    UI1->Payee: payment received notification
```

## Features of RGB Transfers

**The approach adopted by RGB** in transferring consignments between parties, as illustrated in the Alice and Bob example, **underscores the significance of privacy and security**.&#x20;

In the ideal case no one other than Bob and Alice is in possession of the consignment and witness transaction. Nonetheless, Bob has all the elements to verify the validity of the consignment by comparing it with the various anchors on the Bitcoin Blockchain. Bob's stash status is consequently updated through this consignment decomposition and validation procedure. In practical transfer cases, **Alice may publish the witness transaction** to be included in the blockchain **only when some events have occurred**, such as, for example, the transfer of some object from Bob.

At this regard, it's useful to point out that the **RGB system offers a significant advantage over other digital exchange methods, especially when it comes to complex operations such as atomic swaps.** Atomic swaps, commonly used in various cryptocurrency networks, such as the Lightning network, can present complications. Typically, they require two separate transactions and the use of a hash code to ensure that both parties complete the swap almost simultaneously. **This process can create a situation where one party has the power to influence the timing of the exchange by revealing or withholding the hash code, which is known as the** _**reverse American call option problem.**_

**RGB simplifies this issue considerably.** Instead of requiring two separate transactions, **RGB allows the direct exchange of one asset against another (e.g., Bitcoin against an RGB asset or an RGB asset against another RGB asset) within a single transaction**. This eliminates the need for a hash code, as both assets can be exchanged directly. If an exchange involves Bitcoin and RGB assets, both can be included in the same witness transaction output, making the process more direct and secure.

In addition, RGB introduces a **mechanism that allows both parties to have complete control over the execution of the transaction**. If the transaction is not published, both parties have the option to do so, ensuring that neither can take advantage at the expense of the other. If both parties fail to publish, the original inputs can be spent again, rendering the transaction invalid. **This approach offers a higher level of security and flexibility than traditional methods, while simplifying the exchange process.**
