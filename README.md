# edna2qiime

### Code summary

The IPython notebook `edna2qiime.ipynb` performs the following tasks:

1. **Import Libraries**:
   - Imports the `pandas` library.

2. **Load Data**:
   - Loads the first sheet from three Excel files: `studyMetadata`, `sampleMetadata`, and `libraryMetadata`.

3. **Refactor `studyMetadata`**:
   - Selects the last 4 columns of `studyMetadata`.
   - Sets the `field_name` column as the index.
   - Transposes the DataFrame to create `studyMetadataT`.

4. **Extract Unique Sequencing Run IDs and Assay Names**:
   - Extracts unique values of the `seq_run_id` and `assay_name` columns from `libraryMetadata`.

5. **Check Consistency**:
   - Checks if the values of `assay_name` are the same in `studyMetadataT` and `libraryMetadata`.

6. **Merge DataFrames**:
   - Creates a dictionary `merged_dfs` to store the merged DataFrames.
   - Iterates over each combination of `seq_run_id` and `assay_name`:
     - Subsets `libraryMetadata` for the current `seq_run_id` and `assay_name`.
     - Merges the subset of `libraryMetadata` with `sampleMetadata` using `samp_name` as the key.
     - If the merged DataFrame is not empty (i.e., the combination of `seq_run_id` and `assay_name` exists in `libraryMetadata`):
       - Creates a dictionary `new_columns` to hold new columns.
       - Populates `new_columns` with values from `studyMetadataT` for the 'study_level' index, and overrides with values from the `assay` index if they are not NaN.
       - Converts `new_columns` to a DataFrame with the same indexes as the merged DataFrame, repeating the values for each row.
       - Concatenates the new columns DataFrame with the merged DataFrame.
       - Drops columns that contain only NaN values.
       - Adds the merged DataFrame to the `merged_dfs` dictionary.
       - Saves the merged DataFrame to a tab-delimited file named `{runID}.{assay}.txt` without the index column.