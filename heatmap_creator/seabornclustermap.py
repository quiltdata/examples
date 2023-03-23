import argparse
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import scipy

# Define the colorscheme
# ----------------------
# Available colorschemes:
#   https://seaborn.pydata.org/tutorial/color_palettes.html
# Perceptually uniform are best for sequential numeric palattes
# Options are: rocket, mako, flare, crest, magma, viridis
COLORSCHEME = "magma"


# Subset of genes of interest
GENES = [
    "AHRR", "CD27", "CYP1A1", "MYO6", "SLC24A3", 
    "TIPARP", "HIC1", "ITGB3", "BEND7", "DLG5", 
    "PLXDC2", "PRR18", "RND2", "SHF", "STAP2", 
    "FSCN2", "REEP2", "PACSIN3", "SEMA6B", "GPR160", 
    "PHLDA1", "CYP1B1", "ARL4C", "CD93", "STEAP4",
    "ITGA1", "EREG", "KIF5A", "ASB2", "SLC35G5", 
    "BIK", "RARRES2", "SFN", "SHISA8", "GRIN2D", 
    "SNORA5A", "GPR68", "TMPRSS9", "MTFR2", "CLNK", 
    "MYO7B", "CLCN2", "SHISA4", "SATB2", "ADAM11"
]

def generate_clustermap(infile, outfile, verbose):

    if verbose:
        print(f'Running generate_clustermap...')

    # Try importing the data
    try:
        df = pd.read_csv (infile)
    except IOError as e:
        print(e)
        return -1

    if 'ID' in df.columns:
        df = df.loc[df['ID'].isin(GENES)]
        df = df.set_index('ID')
        if verbose:
            print(f'- Pandas message: Data correctly primed for Seaborn plotting.')
    else:
        print("ERROR: Pandas error: The column 'ID' does not exist.")
        return -1

    # Generate the Seaborn clustermap
    # -------------------------------
    # Note there are many clustermap options. For the full list,
    # visit http://seaborn.pydata.org/generated/seaborn.clustermap.html

    # Standardize:
    # cluster_map = sns.clustermap(df, cmap=COLORSCHEME, standard_scale=1)

    # Normalize:
    cluster_map = sns.clustermap(df, cmap=COLORSCHEME, z_score=1)

    # Try to save the figure
    try:
        cluster_map.savefig(outfile)
        if verbose:
            print('- Seaborn message: Figure saved correctly: "{outfile}".')
    except IOError as e:
        print(e)
        print('ERROR: Seaborn error: Figure not saved correctly. See error message above.')
        return -1

    return 0


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate a Seaborn clustermap (dendrogram + heatmap)'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='count',
        default=0,
        help='Verbose output'
    )
    parser.add_argument(
        '-i',
        '--infile',
        dest='infile',
        help='Input data file (relative path)'
    )
    parser.add_argument(
        '-o',
        '--outfile',
        dest='outfile',
        help='Output file (relative path)'
    )

    args = parser.parse_args()
    verbose = args.verbose
    result = generate_clustermap(args.infile, args.outfile, verbose)
    
    if verbose:
        if result == 0:
            print(f'Clustermap successfully generated.')
        elif result == -1:
            print(f'Clustermap generation failed.')
