import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# mentési mappa előkészítése
OUTPUT_DIR = 'charts'
os.makedirs(OUTPUT_DIR, exist_ok=True)


# 0. adatok betöltése és előfeldolgozása
try:
    df = pd.read_csv('imdb_top_1000.csv')
except FileNotFoundError:
    print("Hiba: Az 'imdb_top_1000.csv' fájl nem található a mappában.")
    exit()

# adattípusok konvertálása és tisztítása
df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')
df['Runtime_num'] = df['Runtime'].str.extract(r'(\d+)').astype(float)
df['Gross_num'] = df['Gross'].str.replace(',', '', regex=False).astype(float)
df['Meta_score'] = pd.to_numeric(df['Meta_score'], errors='coerce')
df['Primary_Genre'] = df['Genre'].str.split(',').str[0].str.strip()

print("==================================================")
print("     KOMPLEX IMDb TOP 1000 FILM ADATANALÍZIS")
print("==================================================\n")


# 1. Kérdés: Kritikusok vs. Közönség szakadék
df['Meta_score_10'] = df['Meta_score'] / 10.0
df['Rating_Diff'] = df['IMDB_Rating'] - df['Meta_score_10']

print("1. VÁLASZ: Legnagyobb eltérés a Közönség és Kritikusok között (IMDb vs. MetaScore)")
print(df.nlargest(3, 'Rating_Diff')[['Series_Title', 'IMDB_Rating', 'Meta_score_10', 'Rating_Diff']].to_string(index=False))
print("-" * 65)

# első grafikon
plt.figure(figsize=(9, 5))
scatter = plt.scatter(df['Meta_score_10'], df['IMDB_Rating'], alpha=0.6, c=df['Rating_Diff'], cmap='coolwarm')
plt.plot([4, 10], [4, 10], 'r--', label='Tökéletes egyezés (y=x)')
plt.colorbar(scatter, label='Eltérés (IMDb - MetaScore)')
plt.title('1. Közönségi pontszám (IMDb) vs. Kritikusi pontszám (MetaScore)')
plt.xlabel('MetaScore (10-es skálára átszámítva)')
plt.ylabel('IMDb Pontszám')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '1_critics_vs_audience.png'), dpi=300)
plt.close()


# 2. Kérdés: Rendezői konzisztencia (Átlag vs. Szórás)
director_stats = df.groupby('Director').agg(
    Film_Count=('Series_Title', 'count'),
    Avg_Rating=('IMDB_Rating', 'mean'),
    Rating_Std=('IMDB_Rating', 'std')
)

eligible_directors = director_stats[director_stats['Film_Count'] >= 3].dropna()
top_directors = eligible_directors.sort_values(by=['Avg_Rating', 'Rating_Std'], ascending=[False, True]).head(8)

print("2. VÁLASZ: A legkonzisztensebb elit rendezők (Min. 3 film, magas átlag, alacsony szórás)")
print(top_directors.round(2))
print("-" * 65)

# második grafikon
plt.figure(figsize=(9, 5))
plt.barh(top_directors.index, top_directors['Avg_Rating'], xerr=top_directors['Rating_Std'], color='teal', alpha=0.8, capsize=5)
plt.xlabel('Átlagos IMDb Pontszám (Hibasáv = Szórás)')
plt.title('2. Top Rendezők Átlagpontszáma és Konzisztenciája (Szórása)')
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '2_director_consistency.png'), dpi=300)
plt.close()


# 3. Kérdés: Műfaji elemzés és Bevétel-Értékelés Korreláció
genre_summary = df.groupby('Primary_Genre').agg(
    Avg_Gross=('Gross_num', 'mean'),
    Avg_Rating=('IMDB_Rating', 'mean'),
    Film_Count=('Series_Title', 'count')
).filter(items=df['Primary_Genre'].value_counts()[df['Primary_Genre'].value_counts() > 10].index, axis=0)

print("3. VÁLASZ: Elsődleges műfajok átlagos bevételei (M $)")
print((genre_summary['Avg_Gross'] / 1e6).sort_values(ascending=False).round(2))
print("-" * 65)

# harmadik grafikon
plt.figure(figsize=(9, 5))
(genre_summary['Avg_Gross'] / 1e6).sort_values().plot(kind='barh', color='coral')
plt.title('3. Elsődleges műfajok átlagos bruttó bevétele (Millió USD)')
plt.xlabel('Átlagos Bevétel (Millió $)')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '3_genre_correlations.png'), dpi=300)
plt.close()


# 4. Kérdés: Játékidő Évtizedes Pivot-mátrix
df['Decade'] = (df['Released_Year'] // 10) * 10
df_modern = df[df['Decade'] >= 1950].copy()

bins = [0, 100, 130, 160, 400]
labels = ['Rövid (<100m)', 'Közepes (100-130m)', 'Hosszú (130-160m)', 'Eposzi (160m+)']
df_modern['Runtime_Class'] = pd.cut(df_modern['Runtime_num'], bins=bins, labels=labels)

pivot_runtime = pd.pivot_table(df_modern, values='IMDB_Rating', index='Decade', columns='Runtime_Class', aggfunc='mean')

print("4. VÁLASZ: Játékidő-kategóriák és Évtizedes IMDb Pivot Tábla")
print(pivot_runtime.round(2))
print("-" * 65)

# negyedik grafikon
pivot_runtime.plot(kind='bar', figsize=(10, 5), colormap='tab10')
plt.title('4. Átlagos IMDb Pontszám Játékidő és Évtizedek Szerint')
plt.xlabel('Évtized')
plt.ylabel('Átlagos IMDb Pontszám')
plt.legend(title='Játékidő kategória', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '4_runtime_decade_pivot.png'), dpi=300)
plt.close()


# 5. Kérdés: A 4 Főszereplő összevont elemzése (Melt / Unpivot)
actors_df = df.melt(
    id_vars=['Series_Title', 'IMDB_Rating', 'Gross_num'], 
    value_vars=['Star1', 'Star2', 'Star3', 'Star4'],
    var_name='Star_Position', 
    value_name='Actor'
)

top_actors = actors_df.groupby('Actor').agg(
    Appearance_Count=('Series_Title', 'count'),
    Avg_Gross=('Gross_num', 'mean')
).query('Appearance_Count >= 5').sort_values(by='Avg_Gross', ascending=False).head(8)

print("5. VÁLASZ: Top Színészek átlagos bevétele (Star1-Star4 összevonva, min. 5 film)")
print((top_actors['Avg_Gross'] / 1e6).round(2))
print("-" * 65)

# ötödik grafikon
plt.figure(figsize=(9, 5))
(top_actors['Avg_Gross'] / 1e6).sort_values().plot(kind='barh', color='mediumpurple')
plt.title('5. Legsikeresebb Színészek Filmjeinek Átlagos Bevétele (Min. 5 film)')
plt.xlabel('Átlagos Bevétel (Millió $)')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '5_top_actors.png'), dpi=300)
plt.close()

print(f"\nSikeres futtatás! Az 5 grafikon elmentve a '{OUTPUT_DIR}/' mappába.")
