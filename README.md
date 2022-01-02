![NegBio](https://github.com/yfpeng/negbio2/blob/master/images/negbio.png?raw=true)

-----------------------

[![Build status](https://github.com/bionlplab/negbio2/workflows/negbio2/badge.svg)](https://github.com/bionlplab/negbio2)
[![RTD version](https://img.shields.io/readthedocs/negbio2.svg)](http://negbio2.readthedocs.io)

NegBio is a high-performance NLP tool for negation and uncertainty detection in clinical texts (e.g. radiology reports).


## Update

We are updating the NegBio's pipeline. To use the order version, please see [v0.9.4](https://github.com/ncbi-nlp/NegBio/tree/v0.9.4).


## Get started

1. Download NegBio

    ```bash
    $ git clone https://github.com/bionlplab/negbio2.git
    $ cd /path/to/negbio2
    ```

2. Prepare the dataset. 
   The inputs can be in either plain text or [BioC](http://bioc.sourceforge.net/) format. If the reports are in plain text, each report needs to be in a single file. Some examples can be found in the `examples` folder.

3. Run the script. See [User guide](https://negbio2.readthedocs.io/en/latest/user_guide.html).


## Documentation

Documentation is available from http://negbio2.readthedocs.io

## Contributing

Refer to our [contribution guide](https://negbio2.readthedocs.io/en/latest/contributing.html).


## Citing NegBio

If you're running the NegBio pipeline, please cite:

*  Peng Y, Wang X, Lu L, Bagheri M, Summers RM, Lu Z. [NegBio: a high-performance tool for negation and uncertainty detection in radiology reports](https://arxiv.org/abs/1712.05898). *AMIA 2018 Informatics Summit*. 2018, 188-196.
*  Wang X, Peng Y, Lu L, Bagheri M, Lu Z, Summers R. [ChestX-ray8: Hospital-scale Chest X-ray database and benchmarks on weakly-supervised classification and localization of common thorax diseases](https://arxiv.org/abs/1705.02315). *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*. 2017, 2097-2106.

## Acknowledgments

This work was supported by the Intramural Research Programs of the National Institutes of Health, National Library of Medicine and Clinical Center.

We are grateful to the authors of NegEx, MetaMap, Stanford CoreNLP, Bllip parser, and CheXpert labeler for making their software tools publicly available.

We thank Dr. Alexis Allot for the helpful discussion.

## Disclaimer

This tool shows the results of research conducted in the Computational Biology Branch, NCBI. The information produced on this website is not intended for direct diagnostic use or medical decision-making without review and oversight by a clinical professional. Individuals should not change their health behavior solely on the basis of information produced on this website. NIH does not independently verify the validity or utility of the information produced by this tool. If you have questions about the information produced on this website, please see a health care professional. More information about NCBI's disclaimer policy is available.
