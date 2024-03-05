# Non Inflatable Asset Schema Code Example

In this section we will look more closely to an actual example of an RGB Contract Schema written in Rust and contained in the `nia.rs` file from the [RGB Schemata Repository](https://github.com/RGB-WG/rgb-schemata/blob/master/src/nia.rs) which contain other Schema template as well.  This Schema allows for the contract setup of **non-inflationary fungible assets** **(NIA)** that can be considered as the RGB analogue to Ethereum's fungible tokens created with ERC20 standard.&#x20;

First it's helpful to provide a general layout which is common to all schema.&#x20;

<figure><img src="../../.gitbook/assets/compiled_schema_structure.png" alt="Compiled Schema Structure"><figcaption><p><strong>General Layout of a Schema. Global States and Assignments of Owned States are declared each one preceded by its own Type which make able their referencing in Contract Operations which are declared just after them.  Finally the Validation Scripts and the strict type system used inside the schema are declared.</strong>  </p></figcaption></figure>

We can observe that a Schema can be divided in several general parts:

* An _header_ which contain a Root `SchemaId` which indicates an optional limited form of inheritance from some master schema and a reserved `Feature` field which provides room for additional future extensions of contract schemata.
* A first section in which all the **State Types**  and related variables (both pertaining to [Global](../../rgb-state-and-operations/components-of-a-contract-operation.md#global-state) and[ Assignments](../../rgb-state-and-operations/components-of-a-contract-operation.md#assignments)) and the [Valencies](../../annexes/glossary.md#valency) are declared.
* A second section where all the possible **Contract Operations** referencing the previously declared State Types are encoded
* A field containing the declaration of the **Strict Type System** being used in the whole schema
* A last section containing the validation scripts for all the operations&#x20;

After this layout indication we provide below the actual Rust Code of the schema. Each code section is provided with a numbered reference to an explanation paragraph reported below.

{% code fullWidth="true" %}
```rust
fn nia_schema() -> SubSchema {                      //  --->    (1) 
    // definitions of local variables

    Schema {
        ffv: zero!(),                                                                           // --+                                                      
        subset_of: None,                                                                        //   |  (2) 
        type_system: types.type_system(),                                                       // --+     
        global_types: tiny_bmap! {                                                              // --+
            GS_NOMINAL => GlobalStateSchema::once(types.get("RGBContract.DivisibleAssetSpec")), //   |  
            GS_DATA => GlobalStateSchema::once(types.get("RGBContract.ContractData")),          //   |
            GS_TIMESTAMP => GlobalStateSchema::once(types.get("RGBContract.Timestamp")),        //   |  (3)
            GS_ISSUED_SUPPLY => GlobalStateSchema::once(types.get("RGBContract.Amount")),       //   |
        },                                                                                      // --+
        owned_types: tiny_bmap! {                                               // --+
            OS_ASSET => StateSchema::Fungible(FungibleType::Unsigned64Bit),     //   |  (4)
        },                                                                      // --+                    
        valency_types: none!(),                          // ---+   (5)
        genesis: GenesisSchema {                         //    |
            metadata: Ty::<SemId>::UNIT.id(None),        //    |
            globals: tiny_bmap! {                        //    |
                GS_NOMINAL => Occurrences::Once,         //    |  
                GS_DATA => Occurrences::Once,            //    |
                GS_TIMESTAMP => Occurrences::Once,       //    |
                GS_ISSUED_SUPPLY => Occurrences::Once,   //    |   (6) 
            },                                           //    |
            assignments: tiny_bmap! {                    //    |
                OS_ASSET => Occurrences::OnceOrMore,     //    | 
            },                                           //    |
            valencies: none!(),                          //  --+                 
        },
        extensions: none!(),                             //  --->  (7) 
        transitions: tiny_bmap! {                        //  --+      
            TS_TRANSFER => TransitionSchema {            //    |
                metadata: Ty::<SemId>::UNIT.id(None),    //    |
                globals: none!(),                        //    |
                inputs: tiny_bmap! {                     //    |
                    OS_ASSET => Occurrences::OnceOrMore  //    |   (8)
                },                                       //    |
                assignments: tiny_bmap! {                //    |
                    OS_ASSET => Occurrences::OnceOrMore  //    |
                },                                       //    |
                valencies: none!(),                      //    |
            }                                            //  --+ 
        },
        script: Script::AluVM(AluScript {                                                                 // -+
            libs: confined_bmap! { alu_id => alu_lib },                                                   //  |
            entry_points: confined_bmap! {                                                                // (9)
                EntryPoint::ValidateGenesis => LibSite::with(FN_GENESIS_OFFSET, alu_id),                  //  |
                EntryPoint::ValidateTransition(TS_TRANSFER) => LibSite::with(FN_TRANSFER_OFFSET, alu_id), // -+
            },
        }),
    }
}
```
{% endcode %}

1. It is possible to observe that the `nia_schema()` function has an output of type `SubSchema` which indicates the application an optional single level of inheritance from more general template. This way, a generic Schema that has many useful feature, can be partially reused according to the needs of the issuer.&#x20;
2. In this section `ffv` statement indicates the version of the contract, while `subset_of` statement reflect the optional inheritance from a master contract template described at point 1. `type_system` statement connect the strict type definition to the `StandardType` library of RGB.
3. In this section `global_state` and its variable are declared: in particular:
   * &#x20;The token's `GS_NOMINAL` set of specification which tanks to the strict type library contain inside:
     * &#x20;the token full `name` , the  `ticker`, some additional `details`, the digit `precision`  of the asset.
   * `GS_DATA` containing some additional contract `data` such as a contract disclaimer
   * `GS_TIMESTAMP` referring to the issuance date.
   * `GS_ISSUED_SUPPLY` which defines the maximum cap of the token issuance.
   * The `Once` statement guarantees that all this declaration pertain to an [updatable State rather then an accumulating State](../../rgb-state-and-operations/components-of-a-contract-operation.md#state-update-methods-and-rules).
4. In `owned_type` section, through the `OS_ASSET` statement, we can find the type declaration of the fungible token being transferred through owned state assignment. The quantity of token used in transfer is declared as a [Fungible Type](../../rgb-state-and-operations/components-of-a-contract-operation.md#owned-states) represented by a 64-bit unsigned integer.
5. In this line a declaration of non-existence of valencies for the contract  is made (`valency_types: none!()`)
6. This section of the contract schema marks the beginning of the declaration of Contract Operations starting from the `genesis` :
   * No `metadata` are declared.&#x20;
   * the declaration, inside the Genesis state, of all the variable of the Global State variables previously defined in code section (3).
   * the declaration of the first `assignment` of the token using the previously declared type `OS_ASSET`.
   * No Valencies are declared for this Genesis through the `valencies: none!()`  statement.&#x20;
7. With  `extensions: none!()` statement the schema embeds the absence of any State Extension operation.&#x20;
8. The `transitions` section provide the declaration of a single `TS_TRANSFER` operation which:
   * Contains no `metadata`
   * Doesn't update the global state (it was defined only in genesis)
   * Takes as `inputs`  at leas one or more `OS_ASSET` types.&#x20;
   * Declare the `assignments` of the very same `OS_ASSET` type as those of the inputs.
   * Declare absence of Valencies committed inside the operation.
9. In this final code section we can find the declaration of the a single AluVm `script` which  is responsible to validate:
   * The issuance of the maximum number of token in `genesis`.
   * The validation of each `TS_TRANSFER` operation  where the number of token in `inputs` must match the number declared in the `assignment`

##

##
