#Team 61

1. __Create_Initial_Population.py__: This file will be used to create initial population of size 15 for furthur training of the ML model. The population will be created using the overfit vector.

1. __main.py__: This file will furthur train the Population created by the Create_Initial_Population.py file. The training model is currently set to boost the initial population to 50th generation. You can easily change this in the code. The variable is set on the line 13 of the file.

1. __client.py__:This is the same file as given by the TA's originally to make submission and to get errors for some vector.

1. __parse.py__: This is the same parse file as given by the TA's to check whether our output.json parses correctly or not. 



##generations folder contain generations for the vectors in output.json

1. generation[i] contains ith generation
1. generation[i][0] contains initial population
1. generation[i][1] contains parents
1. generation[i][2] contains children made
1. generation[i][3] contains mutated children
1. generation[i][4] contains next population
