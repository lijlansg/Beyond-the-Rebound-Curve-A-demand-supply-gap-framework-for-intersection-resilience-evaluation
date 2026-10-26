# Beyond the Rebound Curve: A demand-supply gap framework for intersection resilience evaluation

Research data for the intersection resilience evaluation study. This repository contains simulation inputs for metric validation and observed intersection data for the real-world case study.

## Download the complete dataset

Small CSV files and data dictionaries are stored directly in this repository. Large files are supplied as attachments to the [data-v1.0 release](https://github.com/lijlansg/Beyond-the-Rebound-Curve-A-demand-supply-gap-framework-for-intersection-resilience-evaluation/releases/tag/data-v1.0). Downloading GitHub's source-code ZIP alone does **not** include these attachments.

Clone or download this repository, then run the following command from its root with Python 3:

```console
python download_data.py
```

The script downloads the release attachments, checks their SHA-256 hashes, joins split files, decompresses the large CSV files, and restores the original directory layout. Existing valid files are retained. An interrupted download can be resumed by running the same command again.

To download attachments manually, place them together in a local directory and run:

```console
python download_data.py --assets-dir "path/to/downloaded/attachments"
```

After restoration, verify every dataset file with:

```console
python download_data.py --verify-only
```

If a local proxy prevents a connection, the optional `--no-proxy` argument disables proxy use for that invocation. The script requires only the Python standard library. Allow sufficient disk space for both the downloaded attachments and the restored data. The manifest records exact sizes and hashes.

## Data organization

The existing directory and file names are preserved, including their original spelling.

| Directory | Contents |
| --- | --- |
| `For metric validation/Demand surge scenario/` | Demand input and signal schemes for the demand-surge scenarios. |
| `For metric validation/Supply drop scenraio/` | Demand input and signal schemes for the supply-drop scenarios. |
| `Real-wolrd case study/Intersection 57/` | Original trajectory records, original signal schemes, and processed data. |
| `Real-wolrd case study/Intersection 67/` | Original trajectory records, original signal schemes, and processed data. |
| `Real-wolrd case study/Intersection 164/` | Original trajectory records, original signal schemes, and processed data. |
| `Real-wolrd case study/Intersection 170/` | Original trajectory records, original signal schemes, and processed data. |
| `Real-wolrd case study/Intersection 256/` | Original trajectory records, original signal schemes, and processed data. |
| `Real-wolrd case study/Intersection 257/` | Original trajectory records, original signal schemes, and processed data. |

The real-world directory includes `trajectory_data_dictionary.csv`, `signal_data_dictionary.csv`, and `signal_data_description.csv`. Refer to these files for field descriptions. The processed trajectory CSVs contain `rcu_id`, `timestamp`, `uuid`, `latitude`, `longitude`, `heading`, `Direction`, and `Lane`. The processed signal CSVs contain `startTime`, `regionId`, `nodeId`, `phaseId`, `green_ratio`, and `cycle_time_sec`.

## Packaging and integrity

`data-manifest.json` maps every dataset file to its storage location, original size, and SHA-256 hash. `release-SHA256SUMS.txt` lists the hashes of release attachments. Large trajectory CSVs are losslessly gzip-compressed. ZIP files exceeding the attachment size target are split into ordered binary parts. The restoration script produces byte-for-byte copies of the released source files; split ZIP parts must be joined before opening the ZIP.

The release is hosted on GitHub Releases and does not require Git LFS.

## Privacy processing

Before publication, the following fields were removed from all six original trajectory archives: `plateNo`, `lenplateNo`, `plateColor`, and `plateType`. The trajectory record order and the other trajectory fields were retained. Each cleaned archive was read in full and checked for remaining plate-related fields before replacement.

## License

The datasets and accompanying repository materials are licensed under the **Creative Commons Attribution-NonCommercial 4.0 International license (CC BY-NC 4.0)**. Commercial use is not permitted under this license. Noncommercial reuse requires appropriate attribution, a link to the license, and an indication of changes.

See [LICENSE](LICENSE) for the complete terms and the [official license page](https://creativecommons.org/licenses/by-nc/4.0/) for a summary. Please identify this repository and the dataset release when citing or reusing the data.
