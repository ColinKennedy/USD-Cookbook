This repository has a collection of USD snippets and example ideas / concepts.

## Structure summary
Folders
concepts/
 - {CONCEPT_NAME}
  - README.md
   * Snippet
   * Special notes
  - cpp/
  - python/
  - usda/


Each folder in the "concepts" folder shows how to do something in USD.
This is called a "concept".

Each concept folder contains how to do said concept in C++, Python, and
raw USDA syntax.


## How to view
If a concept has a lot of code but only a small part is actually
important, the concept folder may also contain its own README.md which
summarizes the important bits.

Also, look out for lines marked with "XXX". The XXX marker gives further
explanations to what is shown.


## How to build
In the C++ projects, unless otherwise specified, the instructions to
compile and run are ...

```bash
cd {root}/build
cmake ..
make
./build/do_it
```


## Studying
Each concept in the `concepts` folder has a "USD expertise rating"
assigned to it, from 0 (easiest) to 10 (hardest). This repository is
a reference but, if you wand to learn directly from it, the script
below can be used to print out every reference from easiest to hardest.
Theoretically, one could use that to learn USD concepts one at a time.

But note: This repository may not actually show the best way to do
things in USD. It's just a collection of (my) personal findings. Also,
as Pixar comes out with new USD releases and learning resources, this
information may become out-of-date. Always prefer primary guides and
documentation over anything that you see here.

Lastly, I like to keep flashcards for USD. 
My USD deck is [available online here](https://ankiweb.net/shared/decks)


## Final Note
Tested with:
- CentOS 7.6
- USD 19.05
