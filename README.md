# Analyze Delphes native files with bamboo

To install [bamboo](https://gitlab.cern.ch/cp3-cms/bamboo) follow [these instructions](https://bamboo-hep.readthedocs.io/en/latest/install.html).
We will also need a dictionary with the [Delphes](https://cp3.irmp.ucl.ac.be/projects/delphes) classes.
If the same version is not already installed, that can be built with
```bash
cd DelphesIO
cmake -DCMAKE_BUILD_TYPE=Release -DDelphes_VERSION=3.4.2 .
make
```
It is important that the Delphes version matches the one used to write the files.

The example module defined [here](BambooDelphes.py#L74-L86) can be run with
```bash
bambooRun -m BambooDelphes.py:DelphesTest test.yml -o test1
```
What works: accessing the collections, and most of their attributes and member methods; not tested: references to other objects.
