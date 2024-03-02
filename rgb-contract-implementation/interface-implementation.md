# Interface Implementation

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
