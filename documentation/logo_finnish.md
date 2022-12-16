# Logo

Tämä dokumentti sisältää projektin käyttämän Logo-variantin syntaksin ja kieliopin. Osa säännöistä saattaa erota tyypillisestä Logo-kielestä.

- [Datatyypit ja syntaksi](#datatyypit-ja-syntaksi)
- [Viestintä](#viestintä)
- [Robotin liikuttaminen](#robotin-liikuttaminen)
- [Matemaattiset operaatiot](#matemaattiset-operaatiot)
- [Unaariset operaatiot](#unaariset-operaatiot)
- [Vertailuoperaatiot](#vertailuoperaatiot)
- [Ehtolauseet](#ehtolauseet)
    - [Ehtolauseiden näkyvyysalueesta](#ehtolauseiden-näkyvyysalueesta)
- [Muuttujat](#muuttujat)
    - [Muuttujan määrittäminen](#muuttujan-määrittäminen)
    - [Tyypityksestä](#tyypityksestä)
- [Aliohjelmat](#aliohjelmat)
    - [Aliohjelman määrittäminen](#aliohjelman-määrittäminen)
    - [Aliohjelman kutsuminen](#aliohjelman-kutsuminen)
    - [Paluuarvo](#paluuarvo)
    - [Parametrien tyypityksestä](#parametrien-tyypityksestä)
    - [Aliohjelmien näkyvyysalueesta](#aliohjelmien-näkyvyysalueesta)
- [Silmukat](#silmukat)
    - [Silmukoiden näkyvyysalueesta](#silmukoiden-näkyvyysalueesta)
- [Näkyvyysalueet](#näkyvyysalueet)
- [Kirjainlajiriippuvuus](#kirjanlajiriippuvuus)

## Datatyypit ja syntaksi

***"merkkijono***\
***'merkkijono***\
***luku***\
***totuusarvo***

*Esimerkki*
```
tulosta "sana
tulosta 'sana
tulosta 1.23
tulosta 1,23
tulosta joo
tulosta ei
```

***:muuttuja***

*Esimerkki*
```
tulosta :muuttuja
```

***( lauseke )***\
Sulkeita voi käyttää lausekkeiden ryhmittämiseen.

*Esimerkki*
```
tulosta (1 + 2) * 3
```

***aliohjelma param***\
Kutsu aliohjelmaa oletusmäärällä parametrejä.

*Esimerkki*
```
tulosta "sana
```

***( aliohjelma parametri ... )***\
Kutsu aliohjelmaa, joka tukee vaihtelevaa määrää parametreja.

*Esimerkki*
```
(tulosta "hei "maailma)
```

## Viestintä

***tulosta lauseke***\
Kutsua *tulosta* voi käyttää erilaisten arvojen tulostamiseen. *tulosta* tulostaa aina rivinvaihdon, vaikka sille annettaisiin useampi syöte.

*Esimerkki*
```
tulosta "hei
-> hei

tulosta "hei
tulosta "moi
-> hei
-> moi

(tulosta "hei "moi)
-> hei
-> moi
```

## Robotin liikuttaminen
Ohjeet EV3 brickin käyttöönotosta löytyy dokumentaation osasta [Instructions](https://github.com/logo-to-lego/logomotion/blob/main/documentation/instructions.md).

***eteen lauseke***\
***et lauseke***\
Liiku eteenpäin *lauseke* yksikköä.

***taakse lauseke***\
***ta lauseke***\
Liiku taaksepäin *lauseke* yksikköä.

***vasemmalle lauseke***\
***va lauseke***\
Käänny vasemmalle *lauseke* astetta.

***oikealle lauseke***\
***oi lauseke***\
Käänny oikealla *lauseke* astetta.

*Esimerkki*
```
et 100
oi 90
ta 100
va 90
olkoon "x 200
eteen :x
```

## Matemaattiset operaatiot

Matemaattiset operaatiot ovat mahdollisia vain `FLOAT`-tyyppisillä lausekkeilla. Mahdolliset operaatiot ovat `+`, `-`, `*` ja `/`

***lauseke + lauseke***\
summa

***lauseke - lauseke***\
erotus

***lauseke * lauseke***\
kerro

***lauseke / lauseke***\
jaa

## Unaariset operaatiot

Ainoa unaarinen operaatio merkitsee negatiivista lukua ja toimii siksi vain `FLOAT`-tyyppisillä lausekkeilla.

***( - luku )***\
***( - ( lauseke ) )***

*Esimerkki*
```
tulosta (-1)
tulosta (-(1 + 2))
```

## Vertailuoperaatiot

`FLOAT`-tyyppisiä lausekkeita voi vertailla operaattoreilla `<`, `<=`, `>`, `>=`, `=` ja `<>`.

`STRING`-tyyppisiä lausekkeita voi vertailla vain operaattoreilla `=` ja `<>`.

***lauseke < lauseke***\
pienempi kuin

***lauseke <= lauseke***\
pienempi tai yhtä suuri kuin

***lauseke > lauseke***\
suurempi kuin

***lauseke >= lauseke***\
suurempi tai yhtä suuri kuin

***lauseke = lauseke***\
yhtä suuri

***lauseke <> lauseke***\
ei yhtä suuri

## Ehtolauseet

***jos lauseke { komennot }***\
Suorita *komennot*, jos *lauseke* on tosi.

*Esimerkki*
```
jos :x > 999 { tulosta "suuri }
```

***riippuen lauseke { komennot1 } { komennot2 }***\
Suorita *komennot1*, jos *lauseke* on tosi. Muuten suorita *komennot2*.

*Esimerkki*
```
riippuen :x > 999 { tulosta "suuri } { tulosta "pieni }
```

### Ehtolauseiden näkyvyysalueesta
Ehtolauseen ulkopuolella määriteltyihin muuttujiin voi viitata ehtolauseen sisältä.
```
olkoon "x 42
jos :x < 100 {
    tulosta :x
}
```

Ehtolauseilla on kuitenkin oma näkyvyysalueensa. Tämä tarkoittaa sitä, että ehtolauseen sisällä määriteltyihin muuttujiin ei voi viitata ehtolauseen ulkopuolella.

Seuraava koodinpätkä tuottaa virheen, koska muuttujaan *y* viitataan ehtolauseen ulkopuolella.
```
olkoon "x 42
jos :x < 100 {
    olkoon "y 123
}
tulosta :y
-> VIRHE
```

## Muuttujat
Muuttuja määritellään avainsanalla `olkoon` ja kirjoittamalla `"` tai `'` muuttujan nimen eteen. Muuttujan arvo annetaan muuttujan nimen määrittelemisen jälkeen. Muuttujalle *x* voidaan määritellä arvo seuraavalla tavalla: `olkoon "x 42`

Muuttujaan viittaaminen tapahtuu merkillä `:` muuttujan nimen edessä, `:muuttuja`, kuten osassa [Datatyypit ja syntaksi](#datatyypit-ja-syntaksi) määriteltiin. Esimerkkinä yllä olevaan muuttujaan *x* viittaaminen: `tulosta :x` 

### Muuttujan määrittäminen
***olkoon "nimi lauseke***\
Luo muuttuja nimeltään *nimi* ja anna sen arvoksi *lauseke*.

*Esimerkki*
```
olkoon "a 42
```

### Tyypityksestä
Muuttujille asetetaan tyyppi (*luku*, *merkkijono* tai *totuusarvo*) riippuen sille asetetun arvon tyypistä. Tämä Logo-variantti on staattisesti tyypitetty eli muuttujan tyyppiä ei voi muuttaa määrittelyn jälkeen.

*Esimerkki*
```
olkoon "x 10
olkoon "x "viesti
-> VIRHE
```

## Aliohjelmat

### Aliohjelman määrittäminen
***miten aliohjelman.nimi :parametrit ... komennot ... valmis***

*Esimerkki: Aliohjelma **foo** kaksinkertaistaa parametrina saamansa numeerisen arvon **n** ja tulostaa tulon.*
```
MITEN foo :n
    tulosta :n*2
VALMIS
```

Yllä olevaa aliohjelmaa voi kutsua muuttujalla. Esimerkkinä muuttuja x:

```
OLKOON "x 42
foo :x
```

### Aliohjelman kutsuminen
***aliohjelman.nimi argumentit***

*Esimerkki: Suorita aliohjelma **aliohjelma** argumentteina merkkijono **"merkkijono**, muuttuja **:muuttuja** ja luku **2.5**.*
```
aliohjelma "merkkijono :muuttuja 2.5
```

### Paluuarvo
***anna***\
Käytä aliohjelman *komentojen* sisällä antaaksesi aliohjelmalle paluuarvon.

*Esimerkki: Aliohjelma **neliö** antaa parametrinsä **x** neliön.*
```
MITEN neliö :x
    anna :x * :x
VALMIS
```

Paluuarvoa voi käyttää niin kuin mitä tahansa muuta arvoa.
```
olkoon "x neliö 2
olkoon "y (neliö 2) + 5
jos 10 < neliö 5 {}
```

Huomioi, että jos jokin aliohjelman sisäinen näkyvyysalue (kuten ehtolause) sisältää komennon *anna*, niin aliohjelma täytyy myös päättää komennolla *anna*. Alla esimerkki ja ehdotettu korjaus.
```
MITEN foo :x
    jos :x > 1000 {
        anna "liian.kauas
    }
    et :x
VALMIS
-> VIRHE
```
```
MITEN foo :x
    jos :x > 1000 {
        anna "liian.kauas
    }
    et :x
    anna "tarpeeksi.kauas
VALMIS
```

### Parametrien tyypityksestä
Parametrien tyypit täytyy pystyä määrittelemään koodista tai se ei käänny. Useimmiten tämän pystyy tekemään asettamalla parametrille uuden arvon avainsanalla `olkoon` tai käyttämällä [Matemaattisia operaatioita](#matemaattiset-operaatiot) ja [Vertailuoperaatioita](#vertailuoperaatiot).

*Esimerkki: Kääntymätön koodi ja korjausehdotus.*
```
MITEN foo :x
    tulosta :x
VALMIS
-> Muuttujan :x tyyppiä ei ole määritelty
```
```
MITEN foo :x
    tulosta :x+0
VALMIS
```

### Aliohjelmien näkyvyysalueesta
Aliohjelmilla on oma suljettu näkyvyysalueensa. Aliohjelman ulkopuolella määriteltyihin muuttujiin ei ole mahdollista viitata aliohjelman sisältä.
```
olkoon "x 10
MITEN foo
    anna :x
VALMIS
-> VIRHE, muuttujaa :x ei ole määritelty
```
Vastaavasti aliohjelman sisällä määriteltyihin muuttujiin ei ole mahdollista viitata sen ulkopuolella.
```
MITEN foo
    olkoon "x 10
VALMIS
tulosta :x
-> VIRHE, muuttujaa :x ei ole määritelty
```

## Silmukat
***toista lauseke { komennot }***\
Suorita *komennot* *lauseke* kertaa.

*Esimerkki*
```
toista 10 { et 20 }
```

***luvuille [ "muuttuja lauseke lauseke lauseke ] { komennot }***\
Käy luvut alusta loppuun. Argumentit hakasulkeiden sisällä ovat järjestyksessä *muuttuja*, *alku*, *loppu* and *askel*.

*Muuttuja* luodaan uutena paikallisena muuttujana ja siihen voidaan viitata silmukan sisältä samalla tavalla kuin muihin muuttujiin.

*Alku* on arvo, josta *muuttuja* aloittaa.

*Loppu* on arvo, johon *muuttuja* päätyy.

*Askel* on arvo, joka lisätään *muuttujaan* jokaisen *komentojen* suorituskerran jälkeen.

*Esimerkki: Laske 10:een*
```
luvuille ["a 1 10 1] { tulosta :a }
```

*Esimerkki: Tulosta 2:n kertotaulu*
```
luvuille ["a 2 20 2] { tulosta :a }
```

### Silmukoiden näkyvyysalueesta

[Ehtolauseiden näkyvyysalueen](#ehtolauseiden-näkyvyysalueesta) tapaan, silmukan ulkopuolella määriteltyihin muuttujiin voi viitata silmukan sisältä
```
olkoon "x 10
toista 10 { tulosta :x }
luvuille ["i 1 10 1] { tulosta :x }
```
ja silmukoiden sisällä määriteltyihin muuttujiin ei voi viitata niiden ulkopuolella.
```
toista 10 { olkoon "x 10 }
luvuille ["i 1 10 1] { olkoon "y 10 }
tulosta :x
-> VIRHE, muuttujaa :x ei ole määritelty
tulosta :y
-> VIRHE, muuttujaa :y ei ole määritelty
```
**luvuille**-silmukan muuttujaa voi käyttää vain silmukan oman näkyvyysalueen sisällä.
```
luvuille ["i 1 10 1] { tulosta :i }

tulosta :i
-> VIRHE, muuttujaa :i ei ole määritelty
```

## Näkyvyysalueet

Näkyvyysalueiden tiivistämiseksi:

Globaalissa tilassa määriteltyihin muuttujiin ei voi viitata [Aliohjelmien](#aliohjelmat) sisältä. Aliohjelmien sisäisiin tai omiin muuttujiin ei voi viitata globaalissa tilassa.

[Ehtolauseiden](#ehtolauseet) ja [Silmukoiden](#silmukat) sisällä määriteltyihin muuttujiin ei voi viitata niiden ulkopuolella, mutta niiden yläpuolella olevien näkyvyyalueiden sisällä määriteltyihin muuttujiin voi viitata niiden sisältä. Esimerkiksi globaaleihin muuttujiin.

## Kirjanlajiriippuvuus

Muuttujat, komennot, aliohjelmien nimet ja muut viitattavat tietotyypit ovat kirjainlajiriippumattomia. Esimerkiksi:

```
olkoon "x 42
```

Muuttuja `x` määritellään pienillä kirjaimilla, mutta siihen voidaan myöhemmin viitata isoilla kirjaimilla:

```
tulosta :X
-> 42
```

Merkkijonot ovat ainoa poikkeus kirjainlajiriippumattomuuteen.

```
tulosta "kissa = "KISSA
-> ei
```