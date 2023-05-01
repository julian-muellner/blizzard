# Blizzard
Blizzard is an inference and anaylsis tool for probabilistic programs. 

It fully automatically parses the input language, transforms it into a internal Markov chain representation and analyzes the Markov chain using a configurable back-end.
Currently supported back-ends are the probabilistic model checkers Storm and PRISM.

To analyze a program and extract the distribution of a variable, invoke Blizzard by running:

`python3 blizzard.py $BENCHMARK --analyze $VARIABLE`

To configure Blizzard, obtain the Markov chain in PRISM format or find out available options use
`python3 blizzard.py --help`

To facilitate the setup of Storm/PRISM, we provide a [Docker image](https://hub.docker.com/r/jmuellner/blizzard).
