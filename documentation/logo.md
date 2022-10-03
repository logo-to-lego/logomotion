# Logo

Tässä dokumentissa on koostettuna projektissa käytettyjä logo-kielen sääntöjä.

## Muuttujat

Muuttuja määritetään avainsanalla make tai tee, ja antamalla " ennen muuttujan nimeä. Muuttujan arvo annetaan muuttujan nimeämisen jälkeen. Esimerkiksi muuttujalle x annetaan arvo 42
`make "x 42`

Muuttujaan viitataan kaksoispisteellä. Esimerkiksi muuttujan x arvo tulostetaan avainsanalla show, print, sano tai tulosta
`show :x`

## Funktiot

Funktioilla on oma näkyvyysalue, eikä funktion ulkopuolella määriteltyjä muuttujia pysty käyttämään funktion sisällä, ellei niitä anna parametreina. Luodaan esimerkiksi funktio foo, joka tulostaa saamansa parametrin n arvon

```
TO foo :n
  show :n
END
```

Funktiota voidaan kutsua, esimerkiksi muuttujalla x
```
MAKE "x 42
foo :x
```

Funktiota **ei voida** kuitenkaan määritellä ja kutsua näin, sillä funktion ulkopuolella määritellyt muuttujat eivät näy funktion sisälle.
```
TO foo 
  show :x
END

MAKE "x 42
foo
```

## Ehtolauseet

Alla oleva koodi määrittää muuttujan x arvoksi luvun 42. Jos arvo on alle 100, tulostetaan muuttujan x arvo. 
```
make "x 42
if :x < 100 {
    print :x
}
```

Ehtolauseilla on oma näkyvyysalue, eli ehtolauseen sisällä voidaan määrittää muuttujia, jotka eivät näy ehtolauseen ulkopuolelle. Seuraava koodi kaatuu virheeseen, sillä muuttujaan y viitataan ehtolauseen ulkopuolella.
```
make "x 42
if :x < 100 {
    make "y 123
}
show :y
```