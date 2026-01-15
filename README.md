<div align="center">
  <img src="banner_faire2qiime.png" alt="FAIRe2QIIME Banner" width="800">
</div>

# FAIRe2QIIME

This script converts NOAA FAIRe Excel metadata into QIIME2-compatible metadata and manifest files for downstream analysis.

## Features

- Reads project, sample, and experiment-run metadata from an Excel file
- Generates metadata files for each assay (named with marker gene and subfragment)
- Generates manifest files for each sequencing run (named with seq_run_id) and assay (named with marker gene and subfragment)
- Duplicate columns in sample or project metadata will be appended with "_SAMPLE" or "_PROJECT", respectively
- Allows custom column selection for sample names in output metadata files; selected sample name column (e.g., "lib_id") is copied as the first column and named "sample_name" to be compatible with QIIME 2
- Optional suffix handling for duplicate sample names using configurable delimiters and text extraction

## Requirements

- Python 3.7+
- pandas

## Usage

```sh
python faire2qiime.py --path_faire <path_to_excel> --sample_name_column <column_name> --absolute_path_sequences <sequences_dir> --output_directory <output_dir>
```

### Arguments

#### Required Arguments

- `--path_faire` : Path to the FAIRe Excel file containing metadata
- `--sample_name_column` : Column name to use for sample names in output metadata files (example: lib_id)
- `--absolute_path_sequences` : Absolute path to the directory containing sequence files
- `--output_directory` : Directory to save output metadata and manifest files

#### Optional Arguments

- `--column_suffix` : Column name to get suffix from to differentiate samples
- `--direction_suffix` : Side of text to read from to generate suffix (choices: left, right, default: left)
- `--num_chars_suffix` : Number of characters to use for suffix (default: 20)
- `--delimiter_suffix` : Delimiter and any additional text to add before suffix text (default: '_')

### Example

```bash
# Basic usage
python faire2qiime.py \
  --path_faire 'FAIRe-NOAA_myproject.xlsx' \
  --sample_name_column 'lib_id' \
  --absolute_path_sequences '/path/to/folder/with/seq_run_ids' \
  --output_directory .

# Advanced usage with suffix handling for duplicate samples
python faire2qiime.py \
  --path_faire 'FAIRe-NOAA_myproject.xlsx' \
  --sample_name_column 'lib_id' \
  --absolute_path_sequences '/path/to/folder/with/seq_run_ids' \
  --output_directory . \
  --column_suffix 'seq_run_id' \
  --direction_suffix 'right' \
  --num_chars_suffix 8 \
  --delimiter_suffix '_'
```

## Output

- Metadata TSV files for each assay, named like `<project_id>>_<assay_short>_metadata.tsv`
- Manifest TSV files for each sequencing run, named like `<seq_run_id>_<assay_short>_manifest.tsv`

## Troubleshooting

- Ensure all required columns are present in the Excel file
- If you see errors about file paths, check that your sequence directory and filenames are correct
- For pandas import errors, install pandas: `pip install pandas`

## License

[CC0](https://creativecommons.org/public-domain/cc0/)

## Disclaimer

This repository is a scientific product and is not official communication of the National Oceanic and Atmospheric Administration, or the United States Department of Commerce. All NOAA GitHub project code is provided on an 'as is' basis and the user assumes responsibility for its use. Any claims against the Department of Commerce or Department of Commerce bureaus stemming from the use of this GitHub project will be governed by all applicable Federal law. Any reference to specific commercial products, processes, or services by service mark, trademark, manufacturer, or otherwise, does not constitute or imply their endorsement, recommendation or favoring by the Department of Commerce. The Department of Commerce seal and logo, or the seal and logo of a DOC bureau, shall not be used in any manner to imply endorsement of any commercial product or activity by DOC or the United States Government.
