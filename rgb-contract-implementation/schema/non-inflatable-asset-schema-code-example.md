# Non Inflatable Asset Schema Code Example

In this section we are&#x20;

Let's see what the Schema looks like in case we want to define it via some Rust code. Let's take as an example the the relevant part of code contained in the `nia.rs` file contained in the [RGB Schemata  Repository](https://github.com/RGB-WG/rgb-schemata/blob/master/src/nia.rs)  which contain the Schema for **Non non-inflationary fungible assets** that can be considered as the RGB analogue to Ethereum's ERC20 token standard.



We will mark with alphabetically ordered letters the relevant section in the code below providing for each mark a comment paragraph:

{% code fullWidth="true" %}
```rust
fn nia_schema() -> SubSchema {                      //  --+    (1) 
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
            OS_ASSET => StateSchema::Fungible(FungibleType::Unsigned64Bit),     //   |  (3)
        },                                                                      // --+                    
        valency_types: none!(),           
        genesis: GenesisSchema {                         //  --+
            metadata: Ty::<SemId>::UNIT.id(None),        //    |
            globals: tiny_bmap! {                        //    |
                GS_NOMINAL => Occurrences::Once,         //    |  
                GS_DATA => Occurrences::Once,            //    |
                GS_TIMESTAMP => Occurrences::Once,       //    |
                GS_ISSUED_SUPPLY => Occurrences::Once,   //    |   (4) 
            },                                           //    |
            assignments: tiny_bmap! {                    //    |
                OS_ASSET => Occurrences::OnceOrMore,     //    | 
            },                                           //    |
            valencies: none!(),                          //  --|                 
        },
        extensions: none!(),                             //  --+   (5) 
        transitions: tiny_bmap! {                        //  --+      
            TS_TRANSFER => TransitionSchema {            //    |
                metadata: Ty::<SemId>::UNIT.id(None),    //    |
                globals: none!(),                        //    |
                inputs: tiny_bmap! {                     //    |
                    OS_ASSET => Occurrences::OnceOrMore  //    |   (6)
                },                                       //    |
                assignments: tiny_bmap! {                //    |
                    OS_ASSET => Occurrences::OnceOrMore  //    |
                },                                       //    |
                valencies: none!(),                      //    |
            }                                            //  --+ 
        },
        script: Script::AluVM(AluScript {                                                                 // -+
            libs: confined_bmap! { alu_id => alu_lib },                                                   //  |
            entry_points: confined_bmap! {                                                                // (7)
                EntryPoint::ValidateGenesis => LibSite::with(FN_GENESIS_OFFSET, alu_id),                  //  |
                EntryPoint::ValidateTransition(TS_TRANSFER) => LibSite::with(FN_TRANSFER_OFFSET, alu_id), // -+
            },
        }),
    }
}
```
{% endcode %}

1\. We see that the `nia_schema()` function has an output of type `SubSchema`, because with a Schema you can have one level of inheritance. So you can have a generic Schema that does many useful things, but you don't want all of them. You want to have something simpler and you can limit the things it can do and create a sub-Schema as a subset of the more generic Schema, providing additional guarantees. So it is a very specific form of inheritance.

*

After defining the generic `Schema`, if any, to which the Schema you are defining belongs, you define the data type system you are using, `type_system`. This comes from the standard types provided by strict types, `StandardTypes`, extended with `Rgb20`, which is the RGB equivalent of the ERC20 standard, i.e. the standard data type for fungible assets. This data type includes such things as the quantity of tokens, the date and time of issue, the asset specification, i.e., the Rust structure containing the name and precision of the asset. Everything is compiled from the strict types. Whereas in Ethereum, to create a contract that does not allow the ticker to have more than eight characters, we have to write code, for example with Solidity, take the string that contains the ticker, measure the number of characters and consume gas in the process, consuming computing power, in RGB we do not write code. We provide the definition of the restrictions and the type system level. Then we specify that the contract can have a global type which is the token name. And this token name, for its type, is restricted. It has to be longer than one character, but no longer than eight, and each one has to be an ASCII character, and we do this without any scripting, but just using the type system. So we can say that RGB implements functional smart contracts. So we define the global data type `global_types` within which we can define, for example, the nominal. So we can have a nominal value as part of the state and we can have it only once, that is, once it is updated, the last one is discarded. So it is mutable, not accumulable. And it comes from the data type specific structure, which is asset specific. It is a type specification, which has all these fields. So when we rename the assets, we define all these fields. Among other global types we can have: timestamp, total number, supply information and so on. Then we can have a type of `owned_types` which in the example must be a 64-bit unsigned fungible quantity, `FungibleType::Unsigned64Bit`. In the example there is no valency type, `valency_types` is `none`. So this is a very simple scheme, which does not allow us to create secondary emissions, and we can declare it at the scheme level, instead of writing the code in the contract. We can therefore define genesis, transition, and extensions. Genesis can contain metadata, but in this case it does not contain it because we used the unit type, which is always empty data. Also, we notice that in this case there is only one type of state transition, which is transfer. And this transfer, again, has no metadata. It does not define any new global data type. It can only have one type of input, which is a previously owned asset. It can refer to multiple previously owned assets. It can also create new assignments of the type of resource owned, even one or more. And that's it. There is a small validation script with the flood that has only one entry point, validate its own state. This script verifies that the sum of the inputs of the Pedersen commitments is equal to the sum of the outputs of the Pedersen commitments. The power of RGB is that you don't actually have to write the contract this way, because you can write the same thing using YAML or JSON, using the serializer/deserializer to serialize it into the schema object.

## Contract compilation and Issuance

At the moment the Schema can be written in Rust with all the declarative structure and the fields of the contract. After compilation of the schema, The field and the data structure can be  actually filled-in during the subsequent _issuance_ operation in two ways:

* Using  declarative file format such as YAML, JSON using rgb command line tool
* Using a Rust coded issuance

##
