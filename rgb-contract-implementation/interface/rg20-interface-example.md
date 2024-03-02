# RG20 Interface example

## Example code of an RGB20 interface with related implementation

Let's take a closer look at what the Rust code of an interface looks like by taking the example of [standard RGB20](https://github.com/RGB-WG/rgb-std/blob/master/src/interface/rgb20.rs).

{% code fullWidth="true" %}
```rust
fn rgb20() -> Iface {
    let types = StandardTypes::with(rgb20_stl());

    Iface {
        version: VerNo::V1,
        name: tn!("RGB20"),
        global_state: tiny_bmap! {
            fname!("spec") => GlobalIface::required(types.get("RGBContract.DivisibleAssetSpec")),
            fname!("data") => GlobalIface::required(types.get("RGBContract.ContractData")),
            fname!("created") => GlobalIface::required(types.get("RGBContract.Timestamp")),
            fname!("issuedSupply") => GlobalIface::one_or_many(types.get("RGBContract.Amount")),
            fname!("burnedSupply") => GlobalIface::none_or_many(types.get("RGBContract.Amount")),
            fname!("replacedSupply") => GlobalIface::none_or_many(types.get("RGBContract.Amount")),
        },
        assignments: tiny_bmap! {
            fname!("inflationAllowance") => AssignIface::public(OwnedIface::Amount, Req::NoneOrMore),
            fname!("updateRight") => AssignIface::public(OwnedIface::Rights, Req::Optional),
            fname!("burnEpoch") => AssignIface::public(OwnedIface::Rights, Req::Optional),
            fname!("burnRight") => AssignIface::public(OwnedIface::Rights, Req::NoneOrMore),
            fname!("assetOwner") => AssignIface::private(OwnedIface::Amount, Req::NoneOrMore),
        },
        valencies: none!(),
        genesis: GenesisIface {
            metadata: Some(types.get("RGBContract.IssueMeta")),
            global: tiny_bmap! {
                fname!("spec") => ArgSpec::required(),
                fname!("data") => ArgSpec::required(),
                fname!("created") => ArgSpec::required(),
                fname!("issuedSupply") => ArgSpec::required(),
            },
            assignments: tiny_bmap! {
                fname!("assetOwner") => ArgSpec::many(),
                fname!("inflationAllowance") => ArgSpec::many(),
                fname!("updateRight") => ArgSpec::optional(),
                fname!("burnEpoch") => ArgSpec::optional(),
            },
            valencies: none!(),
            errors: tiny_bset! {
                SUPPLY_MISMATCH,
                INVALID_PROOF,
                INSUFFICIENT_RESERVES
            },
        },
        transitions: tiny_bmap! {
            tn!("Transfer") => TransitionIface {
                optional: false,
                metadata: None,
                globals: none!(),
                inputs: tiny_bmap! {
                    fname!("previous") => ArgSpec::from_non_empty("assetOwner"),
                },
                assignments: tiny_bmap! {
                    fname!("beneficiary") => ArgSpec::from_non_empty("assetOwner"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    NON_EQUAL_AMOUNTS
                },
                default_assignment: Some(fname!("beneficiary")),
            },
            tn!("Issue") => TransitionIface {
                optional: true,
                metadata: Some(types.get("RGBContract.IssueMeta")),
                globals: tiny_bmap! {
                    fname!("issuedSupply") => ArgSpec::required(),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_non_empty("inflationAllowance"),
                },
                assignments: tiny_bmap! {
                    fname!("beneficiary") => ArgSpec::from_many("assetOwner"),
                    fname!("future") => ArgSpec::from_many("inflationAllowance"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    SUPPLY_MISMATCH,
                    INVALID_PROOF,
                    ISSUE_EXCEEDS_ALLOWANCE,
                    INSUFFICIENT_RESERVES
                },
                default_assignment: Some(fname!("beneficiary")),
            },
            tn!("OpenEpoch") => TransitionIface {
                optional: true,
                metadata: None,
                globals: none!(),
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("burnEpoch"),
                },
                assignments: tiny_bmap! {
                    fname!("next") => ArgSpec::from_optional("burnEpoch"),
                    fname!("burnRight") => ArgSpec::required()
                },
                valencies: none!(),
                errors: none!(),
                default_assignment: Some(fname!("burnRight")),
            },
            tn!("Burn") => TransitionIface {
                optional: true,
                metadata: Some(types.get("RGBContract.BurnMeta")),
                globals: tiny_bmap! {
                    fname!("burnedSupply") => ArgSpec::required(),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("burnRight"),
                },
                assignments: tiny_bmap! {
                    fname!("future") => ArgSpec::from_optional("burnRight"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    SUPPLY_MISMATCH,
                    INVALID_PROOF,
                    INSUFFICIENT_COVERAGE
                },
                default_assignment: None,
            },
            tn!("Replace") => TransitionIface {
                optional: true,
                metadata: Some(types.get("RGBContract.BurnMeta")),
                globals: tiny_bmap! {
                    fname!("replacedSupply") => ArgSpec::required(),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("burnRight"),
                },
                assignments: tiny_bmap! {
                    fname!("beneficiary") => ArgSpec::from_many("assetOwner"),
                    fname!("future") => ArgSpec::from_optional("burnRight"),
                },
                valencies: none!(),
                errors: tiny_bset! {
                    NON_EQUAL_AMOUNTS,
                    SUPPLY_MISMATCH,
                    INVALID_PROOF,
                    INSUFFICIENT_COVERAGE
                },
                default_assignment: Some(fname!("beneficiary")),
            },
            tn!("Rename") => TransitionIface {
                optional: true,
                metadata: None,
                globals: tiny_bmap! {
                    fname!("new") => ArgSpec::from_required("spec"),
                },
                inputs: tiny_bmap! {
                    fname!("used") => ArgSpec::from_required("updateRight"),
                },
                assignments: tiny_bmap! {
                    fname!("future") => ArgSpec::from_optional("updateRight"),
                },
                valencies: none!(),
                errors: none!(),
                default_assignment: Some(fname!("future")),
            },
        },
        extensions: none!(),
        error_type: types.get("RGB20.Error"),
        default_operation: Some(tn!("Transfer")),
        type_system: types.type_system(),
    }
}
```
{% endcode %}

From Rust code an interface looks very similar to a Schema, but the key difference is that the types are defined in terms of strings, rather than Rust's primitive data types, which are connected directly to the strict data types, see `RGBContract`, that define the semantics for the API. See for example the various transition functions that have meaningful names such as `Transfer`, `Issue` etc... with their equally easily interpretable input arguments such as `input`, `used` etc... which have a data structure of type `assetOwner` defined in the interface itself in a declarative manner. The interface also declares its own error type, `error_type`, and default operation, `default_operation`, which in this case is `Transfer`. Note that, unlike a Schema, in an interface we do not have any AluVM code, since the purpose of the interface does not consist of the business logic of the contract, as mentioned earlier.
