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
```mermaid
graph TD
    A[Input] -- Faculty name --> B[Excel parser]
    A[Input] -- Publication record --> C[Bibtex parser]
    B --> D[Name]
    B --> E[Title]
    B --> F[Year]
    B --> G[Venue: Conf./Journal]
    B --> H[Generate Output which accepts queries]
    C -- record of conf. --> H[Generate Output which accepts queries]
    C -- record of journal --> H[Generate Output which accepts queries]
    H --> I[?q=All - Generate publication record presented in conf. AND journal for all years]
    H --> J[?q=y-Journal - Year wise Journal publication record]
    H --> K[?q=y-Conf. - Year wise Conf. publication record]
    H --> L[?q=y-range - publication record based on custom year duration entered]
```
