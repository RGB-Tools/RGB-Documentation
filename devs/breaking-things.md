# Breaking things

Many things can be broken by a change to the RGB libraries. Here we will try to summarize possible breaks into a set of categories and then for each one of them address the questions of how to mitigate the risks of unnecessary breaking changes - and how to manage breaking changes which can't be avoided.

## Categories of breaking changes

Changes to the codebase can break the following things:

1. **Consensus**. The most serious category, which should be avoided at any cost. RGB consensus has a roadmap for ossification, meaning that at certain point of time it should be impossible to introduce any consensus chages at all. Before we are there, we still can modify consensus under certain conditions, which will be described below.\
   Breaking consensus can be subdivided further into
   * Breaking consensus data serialization
   * Breaking consensus business logic
2. **Network connectivity**, which mean that two applications of diverged versions would not be able to connect and understand each other anymore.
3. **Library API** , meaning that all other libraries and software depending on the libraries containing this type of breaking changes will not be able to compile and will require manual updates to the codebase.
4. **Serialization**, including data storage. It is frequently forgotten that changing just `Debug`, `Display` for `FromStr` implementation even for the data which _are not exposed via Library API_ is a breaking changes, since for instance CI or other integrations may rely on a debug-printed errors from the library. Serialization breaking changes, if missed, also lead to situations where new app versions are not able to read data stored on device, leading to the terrible user expirience.
5. **RPC API**, which leads to the clients not being able to connect and invoke proper procedures from the updated nodes or server-side software. This category is also frequently breaks continious integration scripts, different shell scripts, toolchains etc, so a special attention should be paid for keeping RPC consistent and signal a API version to the clients which connect, such that they will be able to report API incompatibility in a verbose form.

<table><thead><tr><th width="215.33333333333331">What breaks</th><th width="212">Who decides</th><th>Related libraries</th></tr></thead><tbody><tr><td>Consensus</td><td>Consensus maintainers</td><td>Consensus libraries (see "system libraries")</td></tr><tr><td>incl. consensus serialization</td><td>"</td><td><code>confined_encoding</code>, <code>stens</code>, <code>aluvm</code>,<br><code>bp-foundation</code>, <br><code>bp-core</code>, <code>rgb-core</code></td></tr><tr><td>Network connectivity</td><td>Node maintainers</td><td><code>strict_encoding</code>, <code>internet2</code>, <code>cyphernet</code>, <code>lightning_encoding</code>, <code>bp2p</code>, <code>lnp2p</code>, <code>storm-p2p</code></td></tr><tr><td>Library API</td><td>Maintainers of specific library</td><td>Each specific API library</td></tr><tr><td>RPC API</td><td>Node maintainers</td><td>Each specific node or command-line tool</td></tr><tr><td>Data serialization</td><td><em>Depends on application</em></td><td> All</td></tr></tbody></table>

It is important to note that:

* breaking consensus data serialization usually (but not in 100% of cases) breaks everything else as well (network connectivity, library and RPC APIs, data serialization).
* breaking data serialization usually breaks RPC API if these data are transferred through RPC.

## Version number control&#x20;

_**Any**_ breaking change requires major version increase according to the [semantic version number rules](https://semver.org/); i.e. in the first version number component if the major version is `>0` or in the secod version number component if the major number is `0.`

For consensus-level libraries, each library release is followed by a [semversion metadata](https://semver.org/#spec-item-10) specifying the consensus version, for instance `0.8.0+rgb08` or `1.2.0+rgb1`, where pre-release consensus versions are denoted with leading zero.

For libraries which may contain network-level breaking changes `net` metadata followed with networking protocol version is used, for instance `0.9.0+net5`. The same applies to the RPC API with `rpc` metadata; if the same library uses both networking and RPC, than it should contain both, separated with dot (according to semversion rules): `0.9.0+net5.rpc2`.

All other breaking changes (library API and data serialization format) affect only main part of the semantiv version of the library.

The above rules are not being applied to the command-line tools and daemons.
