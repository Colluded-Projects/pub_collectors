## This is a project for SIH2024
If you can see this then the repo is public and our submission was rejected.
## Installation 
Download the zip file from the release section and extract it 
### How to Run
run the app.py using 
```bash
python3 app.py
```
### Dependency

## Credits
<will add your account usernames later.>

## How the app works?
```mermaid
graph TD
    A[Input] --> B[Excel or Bibtex file format]
    B --> C[Run through specific parser] 
    C --> D[Gather the names]
    D --> F[Do web scrapping, gather data :: publication records and citations ::] 
    F --> G[Allow queries]
    G --> H[Display statistics based on query]
    H --> i[Option to Export]
```
