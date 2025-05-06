# PivoScript

## Jak projekt spustit

```
git clone https://github.com/jakubklimo/pivoScript.git
cd pivoScript/project
```

Vše se ovládá pomocí Makefile - make help - zobrazí všechny dostupné operace s Makefile

```
make install                    - Vytvoří virtuální prostředí a nainstaluje závislosti
make build                      - Vygeneruje parser z gramatiky
make / make run                 - Spustí skript s výchozím testovacím souborem
make run FILE=tests/valid.pivo  - Spustí skript se zadaným souborem
make all                        - Spustí vše za vás
make clean                      - Odstraní vygenerované soubory
```

## Co projekt umí

**Proměnné**
```
Decimální
-?[0-9]+
Binární
0b[0-1]+
Hexadecimální
0x[0-9a-f]+
Řetězce  
".*" 

dejmi pivo = 5;
dejmi rum = 0b0010;
dejmi jedno = 2;
dejmi druhy = 1;
dejmi zprava = "Nazdar světe!";  
```

**Operace**
```
+ - jedno + druhý
- - jedno - druhý
* - jedno * druhý
/ - jedno / druhý
```

**Porovnávání**
```
==
<
>
tojejasny (AND)
nebojak (OR)
nenekamo (NOT)
```

**Podmínky, cykly a výstup**
```
výstup:
kecni();
if:
hele (jedno > druhý) {
} jinac {}
Forloop:
jestejedno (i = 0; i < 5; i = i + 1) {
}
```
