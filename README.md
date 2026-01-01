## zot-import 

**A very simple command-line utility to import references into a Zotero library, based on [pyzotero](https://github.com/urschrei/pyzotero).**

It is particularly useful in conjunction with [the Green Frog](https://github.com/redleafnew/zotero-updateifsE) add-on for Zotero, which can be set to automatically update item metadata on import based on a reference's DOI (see [my PR](https://github.com/redleafnew/zotero-updateifsE/pull/203)).
Thus, you (or an agentic coding tool) can run:

```bash
zot-import --doi [DOI] --collection [COLLECTION_ID]
```

and Zotero handles the rest, including automatically updating your .bib file if you are using [Better BibTeX for Zotero](https://github.com/retorquere/zotero-better-bibtex). You can find the [COLLECTION_ID] of your collection by running: 

```bash
pyzotero listcollections
```
