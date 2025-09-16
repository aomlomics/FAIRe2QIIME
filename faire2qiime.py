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
        metadata = df_exptrun[df_exptrun['assay_name'] == assay_name].merge(df_sample, on='samp_name', how='left')
        metadata = pd.merge(metadata, df_project_filled.loc[assay_name].to_frame().transpose(), how='cross')
        metadata.dropna(axis=1, how='all', inplace=True)
        gene = df_project_filled.loc[assay_name]['target_gene'].split(' ')[0]
        subfragment = df_project_filled.loc[assay_name]['target_subfragment']
        subfragment_part = subfragment.split(' ')[0].replace('-', '').replace('_', '') if isinstance(subfragment, str) and subfragment.strip() else ''
        if subfragment_part:
            dict_assay_short[assay_name] = f"{gene}-{subfragment_part}"
        else:
            dict_assay_short[assay_name] = gene
        metadata.to_csv(os.path.join(output_directory, f"{project_id}_{dict_assay_short[assay_name]}_metadata.tsv"), sep='\t', index=False)

    # Manifest file for each seq_run_id
    for seq_run_id in seq_run_ids:
        for assay_name in df_exptrun[df_exptrun['seq_run_id'] == seq_run_id]['assay_name'].unique():
            manifest = df_exptrun[(df_exptrun['seq_run_id'] == seq_run_id) & (df_exptrun['assay_name'] == assay_name)][['samp_name', 'filename', 'filename2']]
            manifest['filename'] = manifest['filename'].apply(lambda x: os.path.join(absolute_path_sequences, f'{seq_run_id}', str(x)))
            manifest['filename2'] = manifest['filename2'].apply(lambda x: os.path.join(absolute_path_sequences, f'{seq_run_id}', str(x)))
            manifest.columns = ['sample-id', 'forward-absolute-filepath', 'reverse-absolute-filepath']
            manifest.to_csv(os.path.join(output_directory, f"{seq_run_id}_{dict_assay_short[assay_name]}_manifest.tsv"), sep='\t', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FAIRe2QIIME CLI: Generate metadata and manifest files from NOAA template.")
    parser.add_argument('--path_faire', required=True, help='Path to FAIRe Excel file')
    parser.add_argument('--absolute_path_sequences', required=True, help='Absolute path to sequences directory')
    parser.add_argument('--output_directory', required=True, help='Directory to save output files')
    args = parser.parse_args()
    main(args.path_faire, args.absolute_path_sequences, args.output_directory)
