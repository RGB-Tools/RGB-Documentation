# Interface and Interface Implementations

An RGB Interface represents a standardized way to define an API for smart contracts. It can be compared to the interfaces of various OOP languages such as Java, but also to traits in Rust, or to the ABIs and ERC standards of smart contracts on Ethereum. However, it differs from Ethereum's ABIs in that they are always included in the contract. Through its use, wallets and other software can provide users with a semantically aware user interface for contract processing. In addition, contract developers can add other interfaces to existing contracts without having to update the contracts themselves (which are immutable).



We anticipated that an interface is both human-readable and wallet-readable information about the contract, the state it is in, and the transactions it can make. The wallet can interact with different contracts using interfaces. So the only thing the wallet has to learn is not the billions of pattern shapes, which can happen, but a small amount of interfaces, which are commonly used. And the interfaces can have a little bit of functionality. They don't necessarily have to cover everything. For example, you can have an interface for a named contract, which just returns the name of the contract or something like that. So it is a fairly composite thing, and the contract can have multiple interfaces to the outside world, which makes things much simpler.

<figure><img src="../../.gitbook/assets/interfaces.png" alt="Interfaces"><figcaption><p><strong>Example of a wallet that interacts with multiple contracts through various interfaces</strong></p></figcaption></figure>

They, therefore, make sense of the different contracts for the user, telling the wallet, first of all, what state the contract has. In addition to the semantic meaning of the state they also provide information on how to parse that state. The only thing the wallet gets through the interface, if you are working with RGB from outside Rust, is a JSON (or YAML) structure, which is self-explanatory, with field names and everything, so that it is easy to make sense of the internal structured data, even if it is complex structures. In addition, the interface tells the wallet what operations can be performed with the contract, what arguments it accepts. Because each argument is structured data, a wallet can also have a way to expose any interface because from the structured data you can generate a form. This means that RGB basically support any smart contract with any interface because of this explanatory layer.

So, a contract can implement many interfaces to provide advanced functionality, and you can update the functionality of the contract and have users be able to use it without asking the wallet developers to update their software. So, for example, suppose you exposed some of it through the standard interface such as RGB20. Unlike Ethereum's ERC20 standard, the contract is created without a single transaction on the blockchain. In fact, you just fill out the form and create a binary object that you then send to other people. So, you can do that and people will see, you will see 20 interfaces in their wallets when they import your contract, but the day after tomorrow you could create a new interface that exposes some other part of the functionality, send it to your users and they will immediately see more of your contract in their wallet without the wallet developers updating or making a new release. What the interface does is it takes the name, then it defines the set of states, like it knows the sum of the states of the contract, and it says these contract-specific state types have these names, and these data types are also bound to the strict type definition. So you basically add semantics to what is already in the contract, and the same thing happens with operations and arguments. So, the interface is a very, very small thing. It's just two mappings.

<figure><img src="../../.gitbook/assets/interface_anatomy.png" alt="Interface anatomy"><figcaption><p><strong>Components of an RGB interface</strong></p></figcaption></figure>

From the above, it is clear that since Schema and Interface are two quite distinct things that can be developed independently, then there must be a way for them to interact. This is what is called _implementing an interface_ for a given Schema. It is for all intents and purposes a map between schema and interface that is mediated by the use of the _strict type system_. An implementation can be compared to Rust's concept of `impl` for structs.

## Interface Implementation code example

Finally we have the [interface implementation](https://github.com/RGB-WG/rgb-schemata/blob/master/src/nia.rs)

```Rust
fn nia_rgb20() -> IfaceImpl {
    let schema = nia_schema();
    let iface = Rgb20::iface();

    IfaceImpl {
        version: VerNo::V1,
        schema_id: schema.schema_id(),
        iface_id: iface.iface_id(),
        script: none!(),
        global_state: tiny_bset! {
            NamedField::with(GS_NOMINAL, fname!("spec")),
            NamedField::with(GS_DATA, fname!("data")),
            NamedField::with(GS_TIMESTAMP, fname!("created")),
            NamedField::with(GS_ISSUED_SUPPLY, fname!("issuedSupply")),
        },
        assignments: tiny_bset! {
            NamedField::with(OS_ASSET, fname!("assetOwner")),
        },
        valencies: none!(),
        transitions: tiny_bset! {
            NamedType::with(TS_TRANSFER, tn!("Transfer")),
        },
        extensions: none!(),
    }
}
```

We see that the implementation takes the Schema, `nia_schema()`, and Interface, `Rgb20::iface()`, and commits them to the id: `schema.schema_id()` and `iface.iface_id()`. Also, we can see how in effect the implementation maps the types defined by the Schema into the types defined in the Interface via the strict types, e.g. `GS_NOMINAL` into `spec`, `GS_DATA` into `data`, etc...
