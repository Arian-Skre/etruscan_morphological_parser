

												*** Etruscan Morphological Parser ***
										A computational framework for Etruscan morphological analysis.


-------------------------------------------------------------------------------------------------------

* Overview:

The Etruscan Morphological Parser (EMP) is a computational linguistics and digital humanities research platform focused on large-scale grammatical analysis of the Etruscan language.
The project is designed to operate across the full known Etruscan corpus (approximately 14,000 inscriptions), using corpus-wide statistical analysis, constrained morphological parsing, positional analysis, and probabilistic evaluation in order to model Etruscan grammatical structures and recurring formulaic patterns.
The parser is not intended to function as a semantic “decipherment engine.” Instead, its primary objective is the computational analysis of:
- morphological structures
- suffix systems
- token relationships
- formulaic syntax
- positional tendencies
- corpus-wide grammatical behaviour
- ritual linguistic recurrence

The long-term goal of the project is to establish a rigorous computational framework capable of supporting:
- large-scale morphological evaluation
- contextual grammatical reconstruction
- probabilistic reconstruction of damaged passages
- corpus-wide syntactic analysis
- statistical identification of recurring linguistic structures

-------------------------------------------------------------------------------------------------------

* Current Version: v0.0.7

-------------------------------------------------------------------------------------------------------

* Current Functionality:

Implemented systems currently include:
- lexical entry storage
- alphabetical lexical organization
- Etruscan numeral parsing
- JSON-based lexical data handling
- structured corpus preparation utilities
- word tokenization
- stem extraction

Although still in early development, the repository is being structured as long-term research infrastructure rather than an isolated parsing experiment.

-------------------------------------------------------------------------------------------------------

* Planned Functionality:

Near-Term Goals:
- suffix decomposition
- number suffix parsing
- case suffix parsing
- morphological segmentation
- multi-hypothesis token parsing
- corpus-wide co-occurrence analysis

Mid-Term Goals:
- probabilistic parsing layers
- local contextual evaluation
- formulaic sequence detection
- ritual syntax modeling
- constraint-driven parse validation
- positional linguistic analysis
- multi-pass parse refinement

Long-Term Goals:
- corpus-scale grammatical modeling
- contextual reconstruction systems
- damaged text reconstruction assistance
- syntactic clustering
- structural alignment across inscriptions
- statistical pattern extraction

-------------------------------------------------------------------------------------------------------

* Research Philosophy:

The Etruscan Morphological Parser is built around several core principles:

1. Grammar Before Semantics
The parser prioritizes grammatical and structural analysis over semantic speculation.
The project does not attempt to produce unrestricted translations or speculative semantic readings. Instead, it focuses on:
- morphological behaviour
- grammatical recurrence
- suffix systems
- syntactic positioning
- statistical relationships across the corpus

2. Corpus-Driven Analysis
No inscription is treated in isolation.
All parsing operations are evaluated against the wider Etruscan corpus using:
- token frequency analysis
- co-occurrence matrices
- positional tendencies
- structural analogues
- recurring formulaic patterns

3. Multi-Hypothesis Parsing
The parser is designed to preserve uncertainty rather than collapse it prematurely.
Each token may retain multiple candidate parses simultaneously, with probabilistic scoring applied across iterative evaluation passes.

4. Constraint-Based Evaluation
Morphological and phonotactic constraints are treated as formal systems.
Both soft and hard constraint modes are planned:
Soft constraints penalize unlikely structures.
Hard constraints disallow invalid constructions.
Comparing both modes allows uncertainty zones and structural divergences to be identified explicitly.

5. Reproducibility and Transparency
Methodology, architecture, and parsing assumptions are documented alongside implementation.
The repository is intended to function as:
computational linguistics infrastructure
digital humanities research software
a reproducible philological analysis framework

-------------------------------------------------------------------------------------------------------

* Research Direction:

The project is intended to support future:
- academic papers
- conference presentations
- collaborative computational philology research
- digital humanities infrastructure development
The long-term objective is the construction of a robust computational framework for evaluating Etruscan grammatical structure at corpus scale.

-------------------------------------------------------------------------------------------------------

* Future Documentation:

Planned documentation includes:
- parsing methodology
- grammar model assumptions
- architecture documentation
- reconstruction theory
- constraint system documentation
- corpus handling standards
- transliteration conventions
- probabilistic scoring methodology

-------------------------------------------------------------------------------------------------------

* Status:

Active research and development.
Early-stage infrastructure build.
Computational morphology framework in progress.
