Dataset **MP IDB** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/2/r/l9/H48oTESu0OkfRfVxl4N6kNHjHewrWCDEwGYzZeR3ozuO4MrNgk5vGLAAlyNkKQGKLIOaB03Q7WNuroQKUcdjGMW3liAyFKtTf93AVC7n4WLZUmNuoh2ylz0WeGZ5.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='MP IDB', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://github.com/andrealoddo/MP-IDB-The-Malaria-Parasite-Image-Database-for-Image-Processing-and-Analysis#mp-idb-the-malaria-parasite-image-database-for-image-processing-and-analysis).