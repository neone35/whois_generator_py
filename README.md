# Whois generator

## Overview
App to generate domain list & fetch whois / availabiltiy data and notify with csv email

## Why this project
I've wondered which domains are taken/available and thought that I'd be great
to integrate with domain generator to automate the process.

## How to run it
1. Make sure you have Python 3+ installed with `python -V`
2. Create `.env` file with your domainr API key:
- Limited (10K req/month) RapidAPI key (get [here](https://rapidapi.com/developer/)) named DOMAINR_RAPIDAPI_KEY
- Unlimited Domainr API (ask them for client_id through ping@domainr.com) named DOMAINR_CLIENT_ID
3. Make sure you have all the dependencies installed at `requirements.txt`
4. Run main file with `python domain_generator.py`
5. Select between generator or scanner options 

## What Did I Learn / Use?
- [Domainr API](https://domainr.com/docs/api)
- Python classes
- Python syntax
- Exception handling
- Terminal GUI operations