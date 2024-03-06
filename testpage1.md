# testpage1

%%{init: {'theme':'forest'}}%%
```mermaid
%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'darkMode': 'false', 
      'primaryColor': '#000000',
      'primaryTextColor': '#c4ffff',
      'primaryBorderColor': '#ffffff',
      'mainBkg': '#000000',
      'lineColor': '#ffffff'
    }
  }
}%%
flowchart BT
    subgraph Merklization
        direction LR
        subgraph MerkleNode
            branching
            depth
            width
            node1
            node2
        end
        MerkleNode -- encode to\ntagged hasher --> MerkleHash
    end
    MerkleHash ---> MerkleNode
    MerkleHash === Root
    Leaf -- commit_id ----> MerkleHash
```



Before Text ...

<figure><img src=".gitbook/assets/csv-shard-1.png" alt=""><figcaption><p>RGB contract shard</p></figcaption></figure>
