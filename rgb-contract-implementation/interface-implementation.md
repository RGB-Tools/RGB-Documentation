# Interface Implementation

## Interface Implementation

From the previous sections, it has been illustrated that every encoded piece of a [contract](../annexes/glossary.md#contract) (such as [Schema](../annexes/glossary.md#schema), [States](../annexes/glossary.md#contract-state) and [Operation](../annexes/glossary.md#contract-operation)) and [Interface](../annexes/glossary.md#interface) are distinct entities that can be developed independently. In order to connect them, an additional piece of code is required. **Interface Implementation represents a simple set of instructions that maps the semantics of the interfaces to the actual strict type data structure of the Schema**.

As a distinctive characteristic, the Interface Implementation can explicitly **map only a subset of the data structure or state operation both from the Schema side and from the Interface side.** This way the interface implementation can restrict implicitly the functionality of some Schema from being accessed as well as it can restrict the use of some endpoints provided in the Interface.

In the following code section, we report the default Interface Implementation which associates [Non-Inflatable Asset Schema](schema/non-inflatable-fungible-asset-schema.md) to the [RGB20 Interface](interface/rgb20-interface-example.md). It is worth pointing out that the following piece of code is placed in the same [file](https://github.com/RGB-WG/rgb-schemata/blob/master/src/nia.rs) as the NIA Schema, but that doesn't represent a mandatory choice as even Interface Implementation can be developed independently from both Schema and Interfaces.

```rust
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

As we can see from the block code above, the Interface Implementation:

* References the Schema, `nia_schema()`, and Interface, `Rgb20::iface()` and commit to them through `schema.schema_id()` and `iface.iface_id()` statements.
* Contains a _map_ between the strict type data structure of the contract (e.g. `GS_NOMINAL` ,`GS_DATA,`etc.) to those of the Interface defined via `fname!` statement (e.g. `"spec"` , `"data"`, etc). The same type of mapping is performed for [contract operations](../annexes/glossary.md#contract-operation), in this case `TS_TRANSFER` is mapped to `"Transfer"`.

The Interface Implementation is compiled separately from Schema and Interface producing a separate `.rgb` or `.rbga` file, which can then be imported in the wallet.
