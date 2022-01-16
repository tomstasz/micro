# micro_train
Projekt składający się z trzech mikroserwisów: pociągu (train), centrali kolejowej (central) i dróżnika (lineman).

## TRAIN
Aplikacja symuluje w sposób uproszczony pracę lokomotywy pociągu. Jej jedynym zadaniem
jest wysyłanie komunikatów na serwer kolejkowy, nie posiada interfejsu HTTP.

- Co 10 sekund wysyłany jest komunikat o aktualnej prędkości pociągu (losowej liczbie z przedziału 0.0-180.0).
- Co 20 sekund wysyłany jest komunikat o stacji do której zbliża się pociąg (pobranej losowo ze zdefiniowanej listy).

## CENTRALA
Centralny ośrodek monitorujący pracę pociągów. Domyślnie nasłuchuje na nowe
komunikaty trafiające na serwer kolejkowy. Na ich podstawie wykonuje określone
reguły biznesowe, nie posiada interfejsu HTTP.

Komunikaty informujące o aktualnej prędkości pociągu wraz z aktualnym czasem
zapisywane są do pliku tekstowego według poniższej reguły:

- wartości z przedziału 0.0-40.0 trafiają do pliku “slow.log”
- wartości z przedziału 40.1-140.0 trafiają do pliku “normal.log”
- wartości z przedziału 140.1-180.0 trafiają do pliku “fast.log”

Komunikaty sygnalizujące, że pociąg zbliża się do stacji są obsługiwane według
poniższego scenariusza:
- Mikroserwis zapisuje w pliku “info.log” czas otrzymania komunikatu.
- Mikroserwis wysyła żądanie typu GET do dróżnika z zapytaniem
  o aktualny stan szlabanu kolejowego.
    - Jeśli szlaban jest otwarty, wysyłane jest żądanie typu POST zamykające
      szlaban.
    - Jeśli szlaban jest zamknięty, zapisuje tą informację w info.log jako anomalię
      i przechodzi do kolejnego podpunktu.
      
- Po 10 sekundach od zamknięcia szlabanu, mikroserwis wysyła żądanie typu
  POST otwierające szlaban.
- Mikroserwis zapisuje w pliku “info.log” czas otwarcia szlabanu.

## DRÓŻNIK
Symuluje w sposób uproszczony pracę dróżnika pilnującego przejazdów kolejowych.
Nie komunikuje się z serwerem kolejkowym, posiada interfejs HTTP.

Aplikacja wystawia poniżej podane url (w nawiasach zostały podane metody
wywołania):

- [GET] /api/v1/barrier - podaje aktualny stan szlabanu w formacie: {“status”:STAN}
- [POST] /api/v1/barrier - otwiera bądź zamyka szlaban bazując na FormData.

Klient wysyła w ciele żądania informację czy bramka ma się otworzyć czy zamknąć.
Aktualny stan szlabanu z ostatnim czasem jego aktualizacji jest przechowywany w bazie danych 
w dedykowanej tabelce.

## URUCHAMIANIE 
W katalogu z docker-compose.yml kontenery projektu uruchamiamy poleceniem
```sh
docker-compose up -d
```
## URUCHAMIANIE LOKALNIE BEZ DOCKERA:
Każdy z procesów uruchamiamy w oddzielnym oknie konsoli.

Odpalamy lokalnie Redis (który bedzie pełnił funkcję brokera).
```sh
redis-server
```
Z poziomu katalogu "train" uruchamiamy workera Celery:
```sh
celery --app=train.tasks.celery worker -Q station,speed --loglevel=info -E
```
oraz schedulera odpowiedzialnego za cykliczne wysyłanie sygnałów
```sh
celery beat --app=train.tasks.celery --loglevel=info
```
Z poziomu katalogu "lineman":
```sh
python3 lineman/main.py
```
Z poziomu katalogu "central":
```sh
python3 central/events.py
```




