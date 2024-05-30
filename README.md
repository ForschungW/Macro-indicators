# Macro-indicators
Proiect final numit ”Combined outlook of selected macroeconomic indicators” pentru cursul pe Python al Sigmoid 2024. 

# Proiect: Combined outlook of selected macroeconomic indicators

## Descriere
Acest proiect Python utilizează Streamlit pentru a afișa grafice ale datelor economice combinate de la două surse: CPI (Indicele Prețurilor de Consum) și PGI (Indicatori Principali Globali), extrase de pe DBnomics și care provin de la Fondul Monetar Internațional. Aplicația permite utilizatorilor să selecteze frecvența, zona de referință și indicatorii pentru fiecare sursă. Datele sunt apoi afișate într-un grafic combinat, iar un model AI analizează graficul. Afișarea datelor depinde de disponibilitatea acestora de la sursă.

## Instalare
1. **Clonați repository-ul:**
   ```bash
   git clone https://github.com/ForschungW/Macro-indicators.git
   cd repository
   ```

2. **Instalați dependențele:**
   Accesați directoriul proiectului în terminal.
   Rulați următoarea comandă pentru a instala toate dependențele
   ```bash
   pip install -r requirements.txt
   ```


## Utilizare
1. **Rulați aplicația Streamlit:**
   ```bash
   streamlit run app.py --server.headless false
   ```

2. **Interfața utilizatorului:**
   - Selectați frecvența, zona de referință și indicatorii pentru sursele CPI și PGI.
   - Selectați perioada de timp pentru care doriți să vedeți datele.
   - Vizualizați graficul combinat și analiza AI a tendințelor grafice.



