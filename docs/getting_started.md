# Getting Started with NegBio

These instructions will get you a copy of the project up and run on your local machine for development and testing purposes. The package should successfully install on Linux (and possibly macOS).

## Installing

### Prerequisites

*  python >3.6
*  Linux
*  Java

Note: since v1.0, MetaMap is not required. You can use the vocabularies (e.g., ``patterns/cxr14_phrases_v2.yml``) instead.

If you want to use MetaMap, it can be downloaded from [https://metamap.nlm.nih.gov/MainDownload.shtml](https://metamap.nlm.nih.gov/MainDownload.shtml).
Installation instructions can be found at [https://metamap.nlm.nih.gov/Installation.shtml](https://metamap.nlm.nih.gov/Installation.shtml).
Please make sure that both ``skrmedpostctl`` and ``wsdserverctl`` are started.

### Setup NegBio

1. Download NegBio
    ```bash
    git clone https://github.com/ncbi-nlp/NegBio.git
    cd /path/to/negbio
    ```
2. Prepare virtual environment
    ```bash
    conda create --name negbio python=3.6
    source activate negbio
    ```
    or
    ```bash
    python3 -m venv negbio
    source negbio/bin/activate
    ```

3. Install required packages
    ```bash
    pip install --upgrade pip setuptools
    pip install -r requirements3.txt
    ```

## Using NegBio

1. Prepare the dataset
    
   The inputs can be in either plain text or [BioC](http://bioc.sourceforge.net/>) format. If the reports are in plain text, each report needs to be in a single file. Some examples can be found in the ``examples`` folder.

2. Run the pipeline

    ```bash
    export OUTPUT_DIR=/path/to/output_dir
    export OUTPUT_LABELS=/path/to/labels
    export INPUT_FILES=/path/to/input_files
    python negbio/negbio_pipeline.py section_split --pattern patterns/section_titles_cxr8.txt --output $OUTPUT_DIR/sections $OUTPUT_DIR/report/* --workers=6
    python negbio/negbio_pipeline.py ssplit --output $OUTPUT_DIR/ssplit $OUTPUT_DIR/sections/* --workers=6
    python negbio/negbio_pipeline.py parse --output $OUTPUT_DIR/parse $OUTPUT_DIR/ssplit/* --workers=6
    python negbio/negbio_pipeline.py ptb2ud --output $OUTPUT_DIR/ud $OUTPUT_DIR/parse/* --workers=4
    python negbio/negbio_pipeline.py dner_regex --phrases_file patterns/chexpert_phrases.yml --output $OUTPUT_DIR/dner $OUTPUT_DIR/ud/* --suffix=.chexpert-regex.xml --workers=6
    python negbio/negbio_pipeline.py neg2 --output $OUTPUT_DIR/neg $OUTPUT_DIR/dner/* --workers=6
    python negbio/ext/chexpert_collect_labels.py --phrases_file patterns/chexpert_phrases.yml --output $OUTPUT_LABELS $OUTPUT_DIR/neg/*
    ```

