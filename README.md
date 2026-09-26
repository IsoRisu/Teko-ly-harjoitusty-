# Teko-ly-harjoitusty-

HUOM:

Olen rikkonut toiminnan kurssin tekoälyalustan kanssa, niin peliä pitää pelata terminaalissa.

Projektin alustaminen:

Lataa kurssin pelitekoälyalusta.

https://github.com/game-ai-platform-team/tira-ai-local/releases

Pura alustan zip tiedosto, navigoi purettuun kansioon terminaalissa ja käynnistä se komennolla ./tira-ai-local

Laita GUI:ssa projektin polku tiraconfig tiedostoon asti. /Teko-ly-harjoitusty-/tiraconfig

Nyt voit pelata peliä.

Unittestaus:

Avaa terminaalissa projektikansio:

Varmista että poetry on alustettuna ja riippuvuudet ajan tasalla.

Sitten voit ajaa: poetry run python -m unittest tests.test_connect4 -v
