# Volná místa 

- skript pro stahování volných pozic z webových stránek českých ministerstev
- velmi hrubá verze
- optimalizováno pro morph.io
- v současné době nestahuje MŽP

## To do - presenation

- [ ] improve documentation - scope and intent
- [ ] update data model documentation

## To do - scope

- [ ] add MZP (waiting for job to appear to learn from)
- [x] add CSSZ
- [x] add NKU
- [x] add FU/FS (could use new functionality - pagination and multi-element titles)
- [x] add UP (requires use new functionality - different-element title and url)
- [ ] add UOOZ (requires new functionality - link-less jobs)
- [ ] add CUZK (not clear about central/regional)
- [ ] add Hygiena
- [x] add MZV

## To do - technical

- [ ] move documentation to wiki
- [ ] programmatically allow for link-less jobs (linking only to general jobs page)
- [x] add fallback for when nothing is found
- [x] implement getting title and url from different elements
- [x] implement getting title from multiple elements
- [x] implement programmatic pagination
- [ ] add error handling
- [x] rewrite scraper routine to take whole dict item as input and deal with the rest
- [x] merge the two input dictionaries
- [ ] document data model for input parameters
- [x] place input data into external json files
- [ ] scope out list of bodies
- [ ] save first-seen and last-seen dates + implement updating instead of duplication
- [x] add fallback for when page not found (e.g. second page of results)
- [x] resolve MD HTTP issue

## Links

- [Scraper a možnost stažení dat](https://morph.io/petrbouchal/GovJobsCZ)
- [Shiny app](http://petrbouchal.shinyapps.io/czjobs)
- [Shiny app na webu Byrokrates](http://byrokrates.cz/praceprostat)



