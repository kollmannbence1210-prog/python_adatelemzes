# IMDb Top 1000 – Haladó Filmipari Adatanalízis

Ez a projekt a Kaggle **IMDb Top 1000 Movies** adathalmazát dolgozza fel `pandas`, `numpy` és `matplotlib` segítségével. A cél a filmtörténet legmagasabbra értékelt alkotásainak elemzése többváltozós statisztikai összefüggések, műfaji sajátosságok, rendezői konzisztencia és közönségi-kritikusi eltérések alapján.

---

##  Használt Technológia és Könyvtárak

- **Python 3.10+**
- **Pandas**: Adattisztítás, unpivot (melt), aggregációk, szórás-számítás, pivot táblák, binning (`pd.cut`)
- **NumPy**: Normálás, feltételes logikai mátrixok, korrelációs számítások
- **Matplotlib**: Vizuális elemzés, grafikonok generálása és automatikus elmentése

---

##  A 5 Összetett Kérdés és Eredményeik

### 1. Kritikusok vs. Közönség (Normált pontszám-szakadék)
*A Meta_score (10-es skálára átszámítva) és az IMDb pontszám eltérésének elemzése.*
![Kritikusok vs Közönség](charts/1_critics_vs_audience.png)

### 2. Rendezői Elit és Konzisztencia
*A legalább 3 filmmel rendelkező rendezők átlagos pontszáma és szórása (`std`).*
![Rendezői Elit](charts/2_director_consistency.png)

### 3. Műfaji Bevétel és Értékelési Korreláció
*Műfajonkénti lineáris korreláció a bruttó bevételek és az IMDb értékelések között.*
![Műfajok Bevétele](charts/3_genre_correlations.png)

### 4. Játékidő "Sweet Spot" Évtizedes Pivot-mátrix
*Hogyan alakult a különböző játékidő-kategóriák (Rövid, Közepes, Hosszú, Eposzi) átlagértékelése az 1950-es évektől napjainkig.*
![Játékidő Pivot](charts/4_runtime_decade_pivot.png)

### 5. A 4 Főszereplő Összevont Elemzése (Unpivot / Melt)
*A 4 főszereplő oszlop (`Star1`..`Star4`) egybefésülése alapján a leggyakrabban feltűnő színészek és filmjeik átlagos bevétele.*
![Top Színészek](charts/5_top_actors.png)

---

##  Telepítés és Futtatás

### 1. Repository klónozása
```bash
git clone [https://github.com/FELHASZNALONEV/imdb-top1000-analysis.git](https://github.com/FELHASZNALONEV/imdb-top1000-analysis.git)
cd imdb-top1000-analysis