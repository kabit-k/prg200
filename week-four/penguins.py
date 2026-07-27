import pandas as pd # import pandas
import seaborn as sns # import seaborn
penguins = sns.load_dataset("penguins")
print(penguins.head())
print("-" * 100)
print(penguins.shape)
print("-" * 100)
print(penguins.dtypes)
print("-" * 100)
print(penguins.isna().sum())

adelie = penguins.loc[penguins["species"] == "Adelie"]
subset_cols = penguins[["species", "island", "body_mass_g"]]
heavy_penguins = penguins.loc[penguins["body_mass_g"] > 4500]

penguins_clean = penguins.dropna(subset=["sex"]).copy()
median_bill = penguins_clean["bill_length_mm"].median()
penguins_clean["bill_length_mm"] = penguins_clean["bill_length_mm"].fillna(median_bill)

avg_mass_by_species = penguins_clean.groupby("species", as_index=False)["body_mass_g"].mean()
avg_flipper_species_sex = (
    penguins_clean.groupby(["species", "sex"], as_index=False)["flipper_length_mm"].mean()
)

print(avg_mass_by_species)
print("*" * 100)
print(avg_flipper_species_sex)

species_lookup = pd.DataFrame(
    {
        "species": ["Adelie", "Chinstrap", "Gentoo"],
        "species_code": ["ADL", "CHS", "GNT"],
    }
)
merged = penguins_clean.merge(species_lookup, on="species", how="left")

pivot = merged.pivot_table(
    values="body_mass_g",
    index="species",
    columns="sex",
    aggfunc="mean",
)

print(merged.head())
print('+' * 100)
print(pivot)