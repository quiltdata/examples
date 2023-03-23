import pandas as pd
import altair as alt

alt.data_transformers.disable_max_rows()

# Colorscheme from https://vega.github.io/vega/docs/schemes/
COLORSCHEME = "viridis"

# Import the data
df = pd.read_csv ('data/vanden_counts.csv')

# The subset of genes Liz is interested in
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


# A random subset of 45 genes not in first group
all_genes = df['ID'].unique()
all_genes_exclude = list(set(all_genes) - set(GENES))

df_group_2 = df.loc[df['ID'].isin(all_genes_exclude)].sample(45)
genes2 = df_group_2.ID.values.tolist()

df_group_1 = df.loc[df['ID'].isin(GENES)]
df_group_2 = df.loc[df['ID'].isin(genes2)]

df_group_1.loc[:, 'GeneGroup'] = "1"
df_group_2.loc[:, 'GeneGroup'] = "2"

df_final = pd.concat([df_group_1, df_group_2])

# "Melt" the data down to a single variable for heatmap
data = df_final.melt(id_vars=['ID', 'GeneGroup'])

genes_dropdown = alt.binding_select(options=["1", "2"], name="Gene Group: ")
genes_select = alt.selection_single(fields=['GeneGroup'], bind=genes_dropdown)

# Generate the Altair plot
alt.Chart(data).mark_rect().encode(
    x = alt.X("variable:N", title="Resection"),
    y = alt.Y("ID:N", title="ID"),
    color = alt.Color("value:Q", title="Value", scale=alt.Scale(scheme=COLORSCHEME)),
    tooltip=['ID', 'variable', 'value', 'GeneGroup']
).interactive(
).add_selection(
    genes_select
).transform_filter(
    genes_select
).save('heatmap.json')
