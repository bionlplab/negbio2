# Installation of NegBio

This part of the documentation covers the installation of NegBio. The first step to using any software package is getting it properly installed.

## Prerequisites

*  python >3.6
*  Linux
*  Java

Note: since v1.0, MetaMap is not required. You can use the vocabularies (e.g., ``patterns/cxr14_phrases_v2.yml``) instead.

If you want to use MetaMap, it can be downloaded from [https://metamap.nlm.nih.gov/MainDownload.shtml](https://metamap.nlm.nih.gov/MainDownload.shtml).
Installation instructions can be found at [https://metamap.nlm.nih.gov/Installation.shtml](https://metamap.nlm.nih.gov/Installation.shtml).
Please make sure that both ``skrmedpostctl`` and ``wsdserverctl`` are started.

## Getting the source code

NegBio is actively developed on GitHub, where the code is [always available](https://github.com/yfpeng/negbio2).

You can clone the public repository

```bash
$ git clone https://github.com/ncbi-nlp/NegBio.git
$ cd negbio
```

Once you have a copy of the source, you can prepare a virtual environment

```bash
$ conda create --name negbio python=3.6
$ source activate negbio
$ pip install --upgrade pip setuptools
```

or

```bash
$ virtualenv --python=/usr/bin/python3.6 negbio_env
$ source negbio_env/bin/activate
```

Finally, you can install the required packages:

```bash
$ pip install -r requirements3.txt
```