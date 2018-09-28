# Nuvarande TODOs i projektet

* ~~Skicka med pipeline_data vid exceptions~~
* ~~Skapa struktur för exceptions (flaggor - retryable etc)~~
* Skapa struktur för caching (för deploys + fel)
  * Bundla ReJSON i compose och använd som cache
  * Snabba upp semver med pagination mot registry/tags - verkar inte funka?
* ~~Bygg stöd för att avbryta en pipeline (next_step = None)~~
* ~~Omarbeta base_pipeline_step~~
* Skriv unit tests för start_deployment_pipelines
* ~~Skriv tests för modules/util~~
* ~~Skriv integration tests~~
* ~~Support för statiska kluster-ipn~~
* Fixa mockade responses så test_complete_pipeline börjar funka igen
* Bygg API
* Lägg till prometheus endpoint ELLER ...
* Pusha metrics till prometheus 
    * Öppna port 9090 i service-lbn
    * Fixa vettiga metrics
    * Möjlighet till konfigurering av server_url:port via env
    * Se: https://prometheus.io/docs/practices/instrumentation/#how-to-instrument
* Definiera ett application objekt som kan skickas vidare till Dizin. Kanske genom CDCs typ Pact? 
```json 
{ 
   "application_name": "KTH Sök",
   "path": "/search/",
   "stack_file": {}
}
```
* Hantera återkoppling från deployments, om det faktiskt startade några containers.
* Ta bort KTH specifika grejor i Dockerfile.
