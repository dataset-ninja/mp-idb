**MP-IDB: Malaria Parasite Image Dataset** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the medical industry. 

The dataset consists of 210 images with 1407 labeled objects belonging to 4 different classes including *falciparum*, *vivax*, *malariae*, and other: *ovale*.

Images in the MP IDB dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There is 1 unlabeled image (i.e. without annotations). There are no pre-defined <i>train/val/test</i> splits in the dataset. Alternatively, the dataset could be split into 4 parasites: ***ring stage*** (125 images), ***trophozoite stage*** (54 images), ***schizont stage*** (38 images), and ***gametocyte stage*** (26 images). The dataset was released in 2019 by the University of Cagliari, Italy, École Polytechnique Fédérale de Lausanne (EPFL), Switzerland, and University of Lausanne and University Hospital Center, Switzerland.

<img src="https://github.com/dataset-ninja/mp-idb/raw/main/visualizations/poster.png">
