# children-linguistic-alignment

children-linguistic-alignment allows to compute the semantic, lexical and syntactic similarity between couples
of consecutive utterances retrieved from the CHILDES database, as well as several other measures.
6 languages available: English, French, Spanish, German, Chinese and Japanese.

## Installation

Install the project by cloning it on your computer or by downloading a compressed version

## Usage

Use the Run notebook, where an example call is already set up

Or you can also run the script run.py

For example: python run.py French_20_25 French 20 25 True
<br />

<ul>
<li>with French_20_25 being the name of the directory where the results will be stored (can be any name) but mandatory</li>
<li>with French being the language used to retrieve data from CHILDES. Mandatory</li>
<li>with 20 being the minimal age to be considered. Mandatory</li>
<li>with 25 being the maximal age to be considered. Mandatory</li>
<li>and True stating if the program is in test mode or not. Optional, default value: False</li>
</ul>

## Contributing
Please contact thomas.misiek@gmail.com to report any bug or if you want to add something to the code

## License
