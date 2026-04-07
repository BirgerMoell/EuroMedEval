# Polish datasets

## Current seed datasets

- `lek-pl`: Polish medical final examination
- `ldek-pl`: Polish dental final examination
- `pes-pl`: Polish specialist board certification exams

## Why they are included

The Polish set is now one of the strongest native benchmark foundations in the repo because it covers:

- physician licensing-style exams
- dentist licensing-style exams
- specialist board certification exams
- many exam years and specialties from a single national source family

## Current EuroMedEval status

- `lek-pl`: `gold`, `unofficial`, `script-only`
- `ldek-pl`: `gold`, `unofficial`, `script-only`
- `pes-pl`: `gold`, `unofficial`, `script-only`

## Notes

The upstream Hugging Face dataset cards state that the exam material was scraped from [CEM](https://www.cem.edu.pl/) and normalized into JSON after excluding image-based and outdated questions. These should be treated as native high-value resources, with careful reporting around redistribution status.
