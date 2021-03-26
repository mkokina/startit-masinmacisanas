import pandas as pd # datu apstrāde
from termcolor import colored as cl # teksta izvade


def info(datne):
    print(cl("\n\nInformācija par datni " + datne, attrs = ['bold']))
    # # importējam datus
    # # df is saīsinajums no Data Frame, 
    # # Pandas bibliotēkas pamata datu struktūras
    df = pd.read_csv(datne)
    # # apskatīt pirmās 5 datu rindiņas
    print(cl("\nPirmās 5 rindiņas", attrs = ['bold']))
    print(df.head(5))
    # # aplūkojam kolonnu nosaukumus
    print(cl("\nKolonnu nosaukumi", attrs = ['bold']))
    print(df.columns)

    # # aplūkojam statistisku informāciju
    print(cl("\nStatistika", attrs = ['bold']))
    print(df.describe())

    print(cl("\nDatu tipi", attrs = ['bold']))
    # aplūkojam datu tipus
    print(cl(df.dtypes, attrs = ['bold']))

    # # parāda, kur datos ir tukšas vērtības
    print(cl("\nTukšas vērtības datos", 'green', attrs = ['bold']))
    print(df.isnull().sum())



datne1 = 'dati/auto_simple.csv'
datne2 = 'dati/auto_imports.csv'

# parādām informāciju par datnē esošajiem datiem
info(datne2)