# Nuvarande TODOs i projektet

* ~~Skicka med pipeline_data vid exceptions~~
* ~~Skapa struktur för exceptions (flaggor - retryable etc)~~
* Skapa struktur för caching (för deploys + fel)
* ~~Bygg stöd för att avbryta en pipeline (next_step = None)~~
* ~~Omarbeta base_pipeline_step~~
* Skriv unit tests
* Skriv tests för modules/util
* ~~Skriv integration tests~~
* ~~Support för statiska kluster-ipn~~
* Bygg API
* Lägg till prometheus endpoint ELLER ...
* Pusha metrics till prometheus 
    * Öppna port 9090 i service-lbn
    * Fixa vettiga metrics
    * Möjlighet till konfigurering av server_url:port via env
    * Se: https://prometheus.io/docs/practices/instrumentation/#how-to-instrument