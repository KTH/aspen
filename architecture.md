# Goals

* General clean up (old code)
* Improve code structure/readability
* Increased testability
* Improve deployment performance
* Improved error handling
* Open source all the things!
* Improve caching and redeployments after fatal errors

# Main loop

* Fetch latest cellus-registry
* Decrypt and load app passwords
* For each docker-stack.yml:
    * Create application object for file
    * Pre deploy hooks
        * Verify cluster for deployment (cellus and application)
        * docker-stack.yml has changed (check cache)
        * New version exists
        * Secrets.env has changed
        * Verify policies (restart, resource, logging)
    * Run service
    * Post deploy hooks
        * Save deployment to cache
        * Send to dizin
        * Send recommendations
        * Information on deployment status/success
