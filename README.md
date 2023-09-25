# isfdb-rdf

The [Internet Speculative Fiction Database (ISFDB)](https://isfdb.org/) is a bibliographic database of publications in science fiction and fantasy and related genres. Its more then 2 million records are catalogued by volunteers sind 1995. This repository contains scripts to convert the publically available [database dump of ISFDB](https://isfdb.org/wiki/index.php/ISFDB_Downloads) into RDF for integration with other data sources.

## Installation

See `Makefile`

Copy `config.example.sh` to `config.sh` and adjust settings.

## Usage

Run `./pubs.py` to convert publications to JSON-LD (not including all fields yet).

## Design considerations

ISFDB uses numeric database identifiers to uniquely refer to entities. The data is available via the HTML interface and database dumps but no official URIs have been defined. The current URIs are equal to ISFDB URLs but they should better be changed to not carry technical details that may change in the future.

## LICENSE

Public Domain
