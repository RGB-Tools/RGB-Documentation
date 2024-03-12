# Contract Implementation in RGB

We have come now to this final  section in which we will be **describing how an RGB contract is actually defined and implemented**. In addition to [Genesis](../annexes/glossary.md#genesis),  which we have discussed [earlier](../rgb-state-and-operations/state-transitions.md#genesis), the definition of  [contract](../annexes/glossary.md#contract) in RGB ecosystem it is realized by  2 +1  independent and complementary components: &#x20;

* [Schema](schema/) which represent the file containing the fundamental contract declarations, states and operatiosn &#x20;
* [Interface](interface/) which contains the instruction to parse the contract and shows state data to users and wallet interface.
* In addition to these components a third one called [Interface Implementation](../annexes/glossary.md#interface-implementation) is responsible to bridge the latter two together. &#x20;

At this regard, it is important to point out that **each one of this component can be freely** and independently developed by different developers, provided that they respect the RGB consensus regarding the validation of client-side data and strict types formats. This represent a notable feature of RGB ecosystem which allows an even higher degree of competition among different components of the contract itself.

In the image below a general scheme of all the components together with a summary explanation is reported. In addition to this, the creation of [genesis](../annexes/glossary.md#genesis) with suitable procedures derived from the 3 components just described and compiled, complete the issuance phase of a contract, which become then fully operational to users.

<figure><img src="../.gitbook/assets/contract_anatomy.png" alt="RGB contract anatomy"><figcaption><p><strong>The list of components which defines a contract in RGB and their analogies with construct of OOP programming languages.</strong></p></figcaption></figure>

In order to give a better general view, the following table summarizes the main characteristics of each one and the  equivalent terminology  adopted both in Object Oriented Programming (OOP) languages and in Ethereum contract system.

<table><thead><tr><th width="220">Contract component</th><th width="129">Meaning</th><th width="162">OOP terms</th><th>Ethereum terms</th></tr></thead><tbody><tr><td>Genesis </td><td>Initial Contract State</td><td>Class constructor</td><td>Contract constructor</td></tr><tr><td>Schema </td><td>Contract business logic</td><td>Class</td><td>Contract</td></tr><tr><td>Interface</td><td>Contract semantics</td><td><p>Interface (Java), </p><p>trait (Rust), protocol (Swift)</p></td><td>ERC* Standard</td></tr><tr><td>Interface Implementation</td><td>Mapping semantics to business logic</td><td>Impl (Rust), Implements (Java)</td><td>Application Binary Interface (ABI)</td></tr></tbody></table>

In the next sections we shall explore in more depth the role and the technicalities of each one of these constructs **which can be written and customized by any person.**