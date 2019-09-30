# Quickstart

Eager to get started? This page gives a good introduction in how to get started with NegBio.

First, make sure that NegBio is installed.


## Preparing the dataset
    
The inputs of NegBio should be in the [BioC](http://bioc.sourceforge.net/>) format. 

Briefly, a BioC-format file is an XML document as the basis of the BioC data exchange and the BioC data classes. Each file contains a group of documents. Each document should have a unique id and one or more passages. Each passage should have (1) a non-overlapping offset that specifies the location of the passage with respect to the whole document, and (2) the original text of the passage. 

The text can contains special characters such as newlines.
   
```xml
<?xml version='1.0' encoding='utf-8' standalone='yes'?>
<collection>
  <source>ChestXray-NIHCC</source>
  <date>2017-05-31</date>
  <key></key>
  <document>
    <id>0001</id>
    <passage>
      <offset>0</offset>
      <text>findings:
chest: four images:
right picc with tip within the upper svc.
probable enlargement of the main pulmonary artery.
mild cardiomegaly.
no evidence of focal infiltrate, effusion or pneumothorax.
dictating </text>
    </passage>
  </document>
  <document>
    <id>0002</id>
    <passage>
      <offset>0</offset>
      <text>findings: pa and lat cxr at 7:34 p.m.. heart and mediastinum are
stable. lungs are unchanged. air- filled cystic changes. no
pneumothorax. osseous structures unchanged scoliosis
impression: stable chest.
dictating </text>
    </passage>
  </document>
</collection>
```

## Running NegBio

```bash
$ export OUTPUT_DIR=examples-local
$ export OUTPUT_LABELS=examples-local/labels.csv
$ export INPUT_FILES="examples/1.xml examples/2.xml"
$ bash examples/run_negbio_examples.sh
```

You can also include all reports in one folder, so that the `$INPUT_FILES=examples/*.xml`

After the script is finished, you can find the labels at `examples-local/labels.csv`. It contains three rows with respect to three documents. Each row has multiple findings, such as Atelectasis and Cardiomegaly. The definition of findings can be found at `patterns/cxr14_phrases_v2.yml`. In this file, 1 means positive findings, 0 means negative findings, and -1 means uncertain findings.

Besides the final label file, there are 6 folders that contain the intermediate files of each step, respectively. For example, the `ssplit` folder consists of sentences, and the `parse` folder consists of parse tree of each sentence. The content and format of these files should be self-explained.

-----

Ready for more? Check out the `User Guide` section.