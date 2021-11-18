# as24_project (Italiano, English below)
### Piccolo progetto di data science per calcolare il prezzo di mercato di un'auto usata e identificare le auto con il miglior rapporto qualita'/prezzo


Il progetto ha avuto origine dalla desiderio di un cliente di vendere la sua vecchia auto per comprarne una elettrica usata. La richiesta si puo' 
sintetizzare nelle seguenti domande:
+ "Voglio vendere la mia vecchia auto benzina/GPL Fiat Punto Evo. Qual'e' il suo prezzo di mercato?"
+ "Voglio acquistare dal mercato dell'usato un'auto elettrica BMW i3. Se dopo un anno di utilizzo non mi piace, voglio rivenderla ad
prezzo che differisce il meno possibile da quello di acquisto. Il altro parole, quali sono le auto con il minor deprezzamento possibile dopo un anno?"

Allo scopo di rispondere a queste domande, abbiamo raccolto i dati relativi alle due auto dal sito autoscout24.it con un codice "spider" e che andremo ad analizzare.

## I files
+ webpage2df.py: Codice Python che fa uso dei pacchetti Selenium e BeautifulSoap per il data scraping
+ as24_analysis.ipynb: prima esplorazione dei dati (EDA, Exploratory Data Analysis) per Fiat Punto Evo
+ as24_BMWi3.ipynb: lo stesso per BMW i3

### Il progetto e' "work in progress..."

----------------------------------------------

# as24_project (English)
### Data science (small) project to compute a fair market price of a second hand car and identify the car(s) with the best quality/price ratio

This project started from the need of a customer to sell his old petrol/LPG car and the will to buy a second hand electric car. 
The customer's questions are:
+ what's the market price of my old car (Fiat Punto Evo)?
+ I want to buy an electric car (BMW i3). If I don't like it, then I want to sell it after one year for a price that differ as less as possible 
to the purchase price. In other words, can you identify which BMW i3 keep at best their value with mileage?

In order to answer to these questions we collected the data by scraping the website Autoscout24.it for the two cars with a "spider" code.
We want to analyse them and building a predictive ML model.

## The files:
+ webpage2df.py: Python code that makes use of Selenium and BeautifulSoap to scrap the data
+ as24_analysis.ipynb: initial EDA for Fiat Punto Evo
+ as24_BMWi3.ipynb: the same for BMW i3

###the work is not completed and in progress...
