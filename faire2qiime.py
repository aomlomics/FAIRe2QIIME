import pandas as pd
import argparse
import os

def main(path_faire, absolute_path_sequences, output_directory):
    df_project = pd.read_excel(path_faire, sheet_name='projectMetadata', comment='#')
    df_sample = pd.read_excel(path_faire, sheet_name='sampleMetadata', comment='#')
    df_exptrun = pd.read_excel(path_faire, sheet_name='experimentRunMetadata', comment='#')

    df_project_first_2_cols_removed = df_project.iloc[:, 2:]
    df_project_first_2_cols_removed.set_index('term_name', inplace=True)
    df_project_wide = df_project_first_2_cols_removed.transpose()
    project_id = df_project_wide['project_id'].iloc[0]
    first_row_values = df_project_wide.loc['project_level']
    df_project_filled = df_project_wide.fillna(first_row_values)

    seq_run_ids = df_exptrun['seq_run_id'].unique()
    assay_names = df_exptrun['assay_name'].unique()
    if set(assay_names) != set(df_exptrun['assay_name'].dropna()):
        raise ValueError("Inconsistent assay names between projectMetadata and experimentRunMetadata.")

    # Metadata file for each assay_name
    dict_assay_short = {}
    for assay_name in df_exptrun['assay_name'].unique():
        # For each assay, merge experiment run metadata with sample metadata and project metadata
        metadata = df_exptrun[df_exptrun['assay_name'] == assay_name].merge(df_sample, on='samp_name', how='left', suffixes=('', '_SAMPLE'))
        metadata = pd.merge(metadata, df_project_filled.loc[assay_name].to_frame().transpose(), how='cross', suffixes=('', '_PROJECT'))
        metadata.dropna(axis=1, how='all', inplace=True)
        metadata.rename(columns={'samp_name': 'sample_name'}, inplace=True)
        
        # Add suffix to sample names that are duplicated within the assay using column_suffix (if provided), direction_suffix, num_chars_suffix, and delimiter_suffix
        # duplicated_samples = metadata['sample_name'][metadata['sample_name'].duplicated(keep=False)].unique()
        # for sample in duplicated_samples:
        #     sample_rows = metadata[metadata['sample_name'] == sample]
        #     for idx, row in sample_rows.iterrows():
        #         suffix = ''
        #         # Currently not implemented: logic to generate suffix based on provided parameters
        #         new_sample_name = f"{row['sample_name']}{suffix}"
        #         metadata.at[idx, 'sample_name'] = new_sample_name
        
        # Short assay name to use for output files
        gene = df_project_filled.loc[assay_name]['target_gene'].split(' ')[0]
        subfragment = df_project_filled.loc[assay_name]['target_subfragment']
        subfragment_part = subfragment.split(' ')[0].replace('-', '').replace('_', '') if isinstance(subfragment, str) and subfragment.strip() else ''
        if subfragment_part:
            dict_assay_short[assay_name] = f"{gene}-{subfragment_part}"
        else:
            dict_assay_short[assay_name] = gene
        metadata.to_csv(os.path.join(output_directory, f"{project_id}_{dict_assay_short[assay_name]}_metadata.tsv"), sep='\t', index=False)
        print(f"Generated metadata file {project_id}_{dict_assay_short[assay_name]}_metadata.tsv")

    # Manifest file for each seq_run_id
    for seq_run_id in seq_run_ids:
        for assay_name in df_exptrun[df_exptrun['seq_run_id'] == seq_run_id]['assay_name'].unique():
            manifest = df_exptrun[(df_exptrun['seq_run_id'] == seq_run_id) & (df_exptrun['assay_name'] == assay_name)][['samp_name', 'filename', 'filename2']]
            manifest['filename'] = manifest['filename'].apply(lambda x: os.path.join(absolute_path_sequences, f'{seq_run_id}', str(x)))
            manifest['filename2'] = manifest['filename2'].apply(lambda x: os.path.join(absolute_path_sequences, f'{seq_run_id}', str(x)))
            manifest.columns = ['sample-id', 'forward-absolute-filepath', 'reverse-absolute-filepath']
            manifest.to_csv(os.path.join(output_directory, f"{seq_run_id}_{dict_assay_short[assay_name]}_manifest.tsv"), sep='\t', index=False)
            print(f"Generated manifest file {seq_run_id}_{dict_assay_short[assay_name]}_manifest.tsv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FAIRe2QIIME CLI: Generate metadata and manifest files from NOAA template.")
    parser.add_argument('--path_faire', required=True, help='Path to FAIRe Excel file')
    parser.add_argument('--absolute_path_sequences', required=True, help='Absolute path to sequences directory')
    parser.add_argument('--output_directory', required=True, help='Directory to save output files')
    parser.add_argument('--column_suffix', required=False, help='Column name to get suffix from to differentiate samples (not implemented)', default=None)
    parser.add_argument('--direction_suffix', required=False, help='Side of text to read from to generate suffixn (not implemented)', choices=['left', 'right'], default='left')
    parser.add_argument('--num_chars_suffix', required=False, type=int, help='Number of characters to use for suffix (not implemented)', default=20)
    parser.add_argument('--delimiter_suffix', required=False, help='Delimiter and optionally prefix text to add before suffix text (not implemented)', default='_')
    args = parser.parse_args()
    main(args.path_faire, args.absolute_path_sequences, args.output_directory)
    