# RGB State


The state represent a set of conditions which are expressed in form of data and which are embedded in the contract itself.

In RGB, this set of data is actually a **set of arbitrary rich data** which:
* are **strongly typed**, which means that **each variable possesses a clear type definition (e.g. u8) and both lower and upped bounds**.
* can be **nested**, meaning that a type can be constructed from other types 
* can be organized in `lists` `sets` or `maps`

An additional element is that the contract states are constructed in order to be **atomic** so that their **ownership** is always a well defined property, which is **reflected in the ownership of the UTxO** embedded in the seal definition.

### Strict Type System

In order to properly encode data into the state in a reproducible way a [Strict Type System]() together with [Strict Encoding]() has been adopted in RGB. This means that:
* The encoding of the data is done according to a precise [schema](#terminilogy/glossary.md#schema) which, unlike JSON or YAML, define a precise structure and layout of the data thus allowing also for deterministic ordering of each data element herein.
* The ordering of the elements inside every collection of elemets (i.e. in lists, sets or maps) is deterministic as well.
* Bounduaries (lower and higher) are defined for every variable and for the number of element in a collection (the so called **Confinement**).
* All data field are byte-alligned.
* The serialization and hashing of the data is performed in a deterministic way (Strict Encoding) allowing for creating **reproducible commitments** of the data irrespective of the system on which such operation is performed.
* The creation of the data according to the schema is **performed through a simple description language which compile in Binary form** from Rust Language. In the future extension to other languages will be supported.
* Additionally, the compiling according to the Strict Type System produces 2 types of outputs:
  * A **Memory Layout at compile time**
  * **Associated Semantic identifiers** to the memory layout (i.e. commitment to each field's name of the data)  
   For instance, this kind of construction is able to make detectable the change of a single variable name, which **doesn't change the memory layout** but which **do change the semantics**.
* Finally, Strict Type System allows for **versioning** of the compilation schema, thus enabling the tracking of consensus changes in contracts and in the compilation engine.
  
In order to have a visual comparison of Strict Encoding with other data structure systems and programming language, the following picture can be useful:

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/d5a1d267-f673-4154-a3d6-3de38b2491a3)

As a matter of fact Strict Encoding is defined in both an extremely pure functional level (thus very far away from Oriented Object Programming (OOP) philosophy) and at a very low level (nearly hardware definition, so far away from more abstract structures and languages).

### Size limitation

The RGB protocol consensus rule apply a **maximum size limit** of 2^16 bite (64kB):
* To the size of **any data type** (e.g. a maximum of 65536 x `u8`, 32768 x `u16`, etc...) 
* To the **number of elements of each collection**, including the collection which represent the state itself (**?**)
This has been designed in order to:
* Avoid unlimited growth of the client side-validate data per each state transition.
* Ensures that this size fits the size of the register of a particular virtual machine [AluVM]() which is capable of complex validation purposes working alonside RGB.

### State components

![image](https://github.com/parsevalbtc/RGB-Documentation/assets/74722637/3f4ad599-558f-4c61-849f-1d6ed7834c40)

#### Transitions Type

In order to describe each component of the RGB state, in the diagram above is represented the complete block layout of an arbitrary type [state transition] which can be one out of 3 **Transition Types**:

* **Genesis**
* **State Transition**
* **State Extension**



The **State**, which is actually the ** New updated State** enforced by a State Transition is constituted by the following components:

* **Assignements** in which are defined:
  * Seals
  * Owned State 
* **Global State**
* **Metadata**
* **Valencies**

The **Old State** is referenced through:
* **Inputs**
* **Redeems** which are a reference to previously defined Valencies


#### Assignements

##### Seals

##### Owned States

#### Global State

#### Metadata

#### Valencies

#### Inputs 

#### Redeems










