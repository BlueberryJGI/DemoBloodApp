"""
author: Jagoda Gotowska
Program analizujący wyniki badan krwi
Do napisania programu korzystano z materiałow z wykladu oraz strony
https://www.pysimplegui.org
https://www.digitalocean.com/community/tutorials/python-find-string-in-list
https://pandas.pydata.org/docs/reference/api/pandas.Series.tolist.html
Dane dla wartości referencyjnych pochodzą ze stron:
https://www.synevo.pl/lipidogram-profil-lipidowy/
https://diag.pl/pacjent/artykuly/morfologia-krwi-co-oznaczaja-wyniki/
https://salve.pl/aktualnosci/badanie-krwi-ob-czym-jest-odczyn-biernackiego-normy-i-interpretacja-wynikow
https://calkiemzdrowo.pl/jak-czytac-wyniki-badan-tarczycy/
https://www.aptelia.pl/czytelnia/a49-Badanie_TSH__jaki_wynik_jest_prawidlowy
https://diag.pl/pacjent/artykuly/crp-marker-stanu-zapalnego/
https://www.aptekaolmed.pl/blog/artykul/morfologia-krwi-na-czym-polega-morfologia-krwi-obwodowej-jak-powinna-wygladac-interpretacja-wynikow-badania-i-jak-przygotowac-sie-na-badanie-krwi,365.html


"""
import PySimpleGUI as sg
import pandas as pd
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('Agg')


wartosci_x=[]#tablica dla typow badan - os x
wartosci_y=[]#tablica dla wartosci wynikow badan - os y
kategorie = ['RBC','HCT','Hb','MCHC','MCH','MCV','RDW','RET','WBC','granulocyty','neutrofile','eozynofile',
             'bazofile','PLT','MONO','LYMPH','limfocyty B','limfocyty T','OB','CRP','TSH',
             'cholesterol calkowity','LDL','HDL','trojglicerydy','glikemia'] #typy badań

#wartosci min i max dla danych plci
wartosci_min_mezczyzni=[4.2,40,14,23,27,82,11.5,0.5,4,1.8,1.5,0.02,0,7.5,0.21,1.1,0.06,0.77,3,0,0.5,0,0,40,
                        0,70]
wartosci_min_kobiety=[3.5,37,12,23,27,82,11.5,0.5,4,1.8,1.5,0.02,0,7.5,0.21,1.1,0.06,0.77,6,0,0.5,0,0,45,0,
                      70]
wartosci_maks_mezczyzni=[5.4,54,18,32,31,93,14.5,1.5,10,8.9,7.4,0.67,0.13,19.5,0.92,3.5,0.66,2.68,8,10,4.1,
                         190,115,1000,150,99]
wartosci_maks_kobiety=[5.2,47,16,32,31,93,14.5,1.5,10,8.9,7.4,0.67,0.13,19.5,0.92,3.5,0.66,2.68,12,10,4.1,
                         190,115,1000,150,99]
jednostki={}
jednostki['cholesterol calkowity']='mg/dl'
jednostki['HDL']='mg/dl'
jednostki['LDL']='mg/dl'
jednostki['trojglicerydy']='mg/dl'
jednostki['glikemia']='mg/dl'
jednostki['granulocyty']='tys./mikrolitr'
jednostki['neutrofile']='tys./mikrolitr'
jednostki['eozynofile']='tys./mikrolitr'
jednostki['bazofile']='tys./mikrolitr'
jednostki['MONO']='tys./mikrolitr'
jednostki['LYMPH']='tys./mikrolitr'
jednostki['limfocyty B']='tys./mikrolitr'
jednostki['limfocyty T']='tys./mikrolitr'
jednostki['OB']='mm/h'
jednostki['TSH']='mIU/l'
jednostki['RBC']='mln/mikrolitr'
jednostki['HCT']='%'
jednostki['RDW']='%'
jednostki['RET']='%'
jednostki['Hb']='g/l'
jednostki['MCHC']='g/dl'
jednostki['MCH']='pg'
jednostki['MCV']='fl'
jednostki['PLT']='fl'
jednostki['WBC']='tys./mikrolitr'

def recznie():
    """Funkcja odpowiedajaca za dzialanie dodatkowego okienka, w ktorym deklaruje sie recznie wyniki badan"""

    ukladzik=[[sg.Text('Wybierz typ badań:'),sg.Listbox(kategorie,size=(20,3),key='typ_badan')],
              [sg.Text('Wpisz wynik badań:'),sg.InputText(key='wyniki_badan')],
              [sg.Button('Dodaj dane'),sg.Button('Zakończ dodawanie')]]
    okienko = sg.Window('Dane wpisywane ręcznie', ukladzik)
            
    while True:
        zdarzenie, wartosci = okienko.read()

        if zdarzenie == 'Dodaj dane':
            wynik_pisemnie(wartosci['typ_badan'],wartosci['wyniki_badan'])
            
        if zdarzenie == 'Zakończ dodawanie':
            break


        if zdarzenie == sg.WIN_CLOSED:
            break

    okienko.close()
    return

def wynik_pisemnie(x,y):
    """Funkcja pozwalajaca na dodanie nastepnych wynikow badan krwi
       
       Args: x(string): typ badań jakie chcemy dodać do porównania
             y(float): wartość badań, jaką chcemy dodać
    """
    iksowa=x[0]
    igrekowa=float(y)
    if iksowa in wartosci_x:
        wpisane_ponownie(iksowa,igrekowa)
        return
    else:
        wartosci_x.append(iksowa)
        wartosci_y.append(igrekowa)
    return


def wpisane_ponownie(x,y):
    """Funkcja zglaszajaca uzytkownikowi, ze juz raz recznie wpisal poprzednie dane"""

    uklad_maly=[[sg.Text('Próbujesz wpisac wynik dla wcześniej zapisanych danych.')],
                [sg.Button('Nadpisz'),sg.Button('Anuluj')]]

    okieneczko = sg.Window('UWAGA',uklad_maly)

    while True:
        zdarzenie, wartosci = okieneczko.read()

        #nadpisanie wczesniej zapisanych danych
        if zdarzenie == 'Nadpisz':
            for i in range(len(wartosci_x)):
                if wartosci_x[i] == x:
                    wartosci_y[i] == y
                    okieneczko.close()
                

        if zdarzenie == sg.WIN_CLOSED or zdarzenie == 'Anuluj':
            break
    
    okieneczko.close()

    return

def porownanie_reczne(jaka_plec):
    """Funkcja umożliwiająca porównanie wyników wpisanych ręcznie z danymi referencyjnymi"""

    zliczanie_min = 0
    zliczanie_maks = 0
    za_wysokie=[]
    za_niskie=[]

    if wartosci_x == []:
        uklad_porownanie = [[sg.Text('Brak wpisanych wyników'), sg.Button('Zamknij')]]
        okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
        while True:
            zdarzenie, wartosci = okno_porownanie.read()
            if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                break
        okno_porownanie.close()
        return

    if jaka_plec == 'mężczyzna':
        for i in range(len(wartosci_x)):
            for j in range(len(kategorie)):
                if wartosci_x[i] == kategorie[j]:
                    if wartosci_y[i] > wartosci_maks_mezczyzni[j]:
                        zliczanie_maks += 1
                        za_wysokie.append(wartosci_x[i])
                    elif wartosci_y[i] < wartosci_min_mezczyzni[j]:
                        zliczanie_min += 1
                        za_niskie.append(wartosci_x[i])
    else:
        for i in range(len(wartosci_x)):
            for j in range(len(kategorie)):
                if wartosci_x[i] == kategorie[j]:
                    if wartosci_y[i] > wartosci_maks_kobiety[j]:
                        zliczanie_maks += 1
                        za_wysokie.append(wartosci_x[i])
                    elif wartosci_y[i] < wartosci_min_kobiety[j]:
                        zliczanie_min += 1
                        za_niskie.append(wartosci_x[i])

    niskie=''
    for i in range(len(za_niskie)):
        niskie+=za_niskie[i]
        if i< (len(za_wysokie)-1):
            niskie+=', '

    wysokie=''
    for i in range(len(za_wysokie)):
        wysokie+=za_wysokie[i]
        if i < (len(za_wysokie)-1):
            wysokie+=', '

    if zliczanie_min == 0:
        if zliczanie_maks == 0:
            uklad_porownanie = [[sg.Text('Wyniki są poprawne'), sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()
                    
        else:
            uklad_porownanie = [[sg.Text('Wyniki nie są poprawne. Zbyt wysokie wartości ma: '+wysokie), 
                                 sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()
    else:
        if zliczanie_maks == 0:
            uklad_porownanie = [[sg.Text('Wyniki nie są poprawne. Za niskie wartości ma:'+niskie),
                                  sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()
        else:
            uklad_porownanie = [[sg.Text('Zbyt niskie wyniki dla: '+niskie+'. Zbyt wysokie wyniki dla: '+
                                          wysokie), sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()

    return

def porownanie_plik(plik,jaka_plec):
    """Funkcja wczytujaca dane badan z pliku csv"""

    dane=pd.read_csv(plik,delimiter=';')

    iksowe_plik=dane['Badanie'].tolist()
    for i in range(len(iksowe_plik)):
        wartosci_x.append(iksowe_plik[i])

    igrekowe_plik=dane['Wynik'].tolist()
    for i in range(len(igrekowe_plik)):
        wartosci_y.append(igrekowe_plik[i])

    zliczanie_min = 0
    zliczanie_maks = 0
    za_wysokie=[]
    za_niskie=[]

    if iksowe_plik == []:
        uklad_porownanie = [[sg.Text('Brak wpisanych wyników'), sg.Button('Zamknij')]]
        okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
        while True:
            zdarzenie, wartosci = okno_porownanie.read()
            if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                break
        okno_porownanie.close()
        return

    if jaka_plec == 'mężczyzna':
        for i in range(len(iksowe_plik)):
            for j in range(len(kategorie)):
                if iksowe_plik[i] == kategorie[j]:
                    if igrekowe_plik[i] > wartosci_maks_mezczyzni[j]:
                        zliczanie_maks += 1
                        za_wysokie.append(iksowe_plik[i])
                    elif igrekowe_plik[i] < wartosci_min_mezczyzni[j]:
                        zliczanie_min += 1
                        za_niskie.append(iksowe_plik[i])
    else:
        for i in range(len(iksowe_plik)):
            for j in range(len(kategorie)):
                if iksowe_plik[i] == kategorie[j]:
                    if igrekowe_plik[i] > wartosci_maks_kobiety[j]:
                        zliczanie_maks += 1
                        za_wysokie.append(iksowe_plik[i])
                    elif igrekowe_plik[i] < wartosci_min_kobiety[j]:
                        zliczanie_min += 1
                        za_niskie.append(iksowe_plik[i])

    niskie=''
    for i in range(len(za_niskie)):
        niskie+=za_niskie[i]
        if i< (len(za_wysokie)-1):
            niskie+=', '

    wysokie=''
    for i in range(len(za_wysokie)):
        wysokie+=za_wysokie[i]
        if i < (len(za_wysokie)-1):
            wysokie+=', '

    if zliczanie_min == 0:
        if zliczanie_maks == 0:
            uklad_porownanie = [[sg.Text('Wyniki są poprawne'), sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()
                    
        else:
            uklad_porownanie = [[sg.Text('Wyniki nie są poprawne. Zbyt wysokie wartości ma: '+wysokie), 
                                 sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()
    else:
        if zliczanie_maks == 0:
            uklad_porownanie = [[sg.Text('Wyniki nie są poprawne. Za niskie wartości ma:'+niskie),
                                  sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()
        else:
            uklad_porownanie = [[sg.Text('Zbyt niskie wyniki dla: '+niskie+'. Zbyt wysokie wyniki dla: '+
                                          wysokie), sg.Button('Zamknij')]]
            okno_porownanie = sg.Window('Przeanalizowane wyniki',uklad_porownanie)
            while True:
                zdarzenie, wartosci = okno_porownanie.read()

                if zdarzenie == 'Zamknij' or zdarzenie == sg.WINDOW_CLOSED:
                    break
            okno_porownanie.close()
    

    return

def rysowanie(x,jaka_plec):
    """Funkcja odpowiadająca za rysowanie wykresu na podstawie wybranej kategorii"""


    sprawdzenie = False
    sprawdzenie_drugie=x[0]

    for i in range(len(wartosci_x)):
        if sprawdzenie_drugie == wartosci_x[i]:
            sprawdzenie = True
            break
    if not sprawdzenie:
        uklad_blad=[[sg.Text('Brak danych - nie można wykonać rysunku')],[sg.Button('Zamknij')]]
        okno_blad=sg.Window('Okno błędu',uklad_blad)

        while True:
            zdarzenie, wartosci = okno_blad.read()

            if zdarzenie == 'Zamknij' or zdarzenie == sg.WIN_CLOSED:
                break
        okno_blad.close()
    else:
        if jaka_plec == 'mężczyzna':
            for i in range(len(wartosci_x)):
                for j in range(len(kategorie)):
                    if sprawdzenie_drugie == wartosci_x[i]:
                        minimum = wartosci_min_mezczyzni[j]
                        maksimum = wartosci_maks_mezczyzni[j]
                        szukana = wartosci_y[i]
                        break
        else: 
            for i in range(len(wartosci_x)):
                    for j in range(len(kategorie)):
                        if sprawdzenie_drugie == wartosci_x[i]:
                            minimum = wartosci_min_kobiety[j]
                            maksimum = wartosci_maks_kobiety[j]
                            szukana = wartosci_y[i]
                            break            
                    
    x_wykres=['minimum','maksimum',sprawdzenie_drugie]   
    y_wykres=[minimum,maksimum,szukana]           
    os_y=jednostki[sprawdzenie_drugie]
    
    plt.cla()
    plt.bar(x_wykres,y_wykres)
    plt.xlabel('Wartości referencyjne oraz wynik')
    plt.ylabel(os_y)
    plt.title('Porównanie wyników z wartościami referencyjnymi')

    


    return

def zapisywanie(tytul):
    """Funkcja pozwalające na zapisanie wykresu na podstawie otrzymanych badań."""

    tytul_string=tytul[0]
    plt.savefig('Wynik badań '+ tytul_string+ '.pdf')

    return

def main():
    """Funkcja glowna programu"""

    plec = ['kobieta','mężczyzna']
    
    z_pliku=False

    #tworzenie ukladu okna programu
    uklad = [[sg.Text('Określ płeć:'),sg.Listbox(plec,size=(10,2),key='płeć')],
             [sg.Text('Wybrany plik csv z wynikami badań:')],
             [sg.InputText(key='nazwa_pliku'),sg.FileBrowse('Wyszukaj...', target='nazwa_pliku'),
              sg.Button('Otwórz'),sg.Button('Dodaj wynik ręcznie')],
             [sg.Button('Zatwierdź wprowadzone wyniki do analizy')],
             [sg.Text('Wybierz wyniki do porównania na wykresie: '),sg.Listbox(kategorie,size=(12,3),
              key='do_wykresu'),sg.Button('Utwórz wykres')],
             [sg.Canvas(key='plotno',size=(400,300),background_color='white')],
             [sg.Button('Zapisz wykres'),sg.Text('Copyright: Jagoda Gotowska')]]

    okno = sg.Window('Analiza wyników badań krwi', uklad,finalize=True)
    rysunek=plt.figure()
    plotno_rysunku = FigureCanvasTkAgg(rysunek,okno['plotno'].TKCanvas)
    plotno_rysunku.get_tk_widget().pack()
    
    #glowna petla wykonujaca do glownego okna
    while True:
        zdarzenie, wartosci = okno.read()
        
        #warunkowanie wyłączenia programu
        if zdarzenie == sg.WIN_CLOSED:
            break

        #dodanie wynikow recznie w osobnym okienku
        if zdarzenie == 'Dodaj wynik ręcznie':
            recznie()
           
        #wczytanie danych badan z pliku csv   
        if zdarzenie == 'Otwórz':
            z_pliku=True

        #wykonanie porównania i wykresu
        if zdarzenie == 'Zatwierdź wprowadzone wyniki do analizy':

            if z_pliku == True:
                porownanie_plik(wartosci['nazwa_pliku'],wartosci['płeć'])
            else:
                porownanie_reczne(wartosci['płeć'])

        if zdarzenie == 'Utwórz wykres':
            rysowanie(wartosci['do_wykresu'],wartosci['płeć'])
            plotno_rysunku.draw()

        #zapisywanie wykresu
        if zdarzenie == 'Zapisz wykres':
            zapisywanie(wartosci['do_wykresu'])
            
            
    
    plt.close(rysunek)
        
    okno.close()
    return

main()