# Cheat on Tusmo!
*Why would I cheat on tusmo?*
For no reason at all, it's fun!

I've been in the last few weeks very exposed to the online game [Tusmo](www.tusmo.xyz), and I thought it would be a fun project
to make a script that would help you out (give you the answers).

Just clone, and run `main.py`.

## Using other dictionaries
The program uses a .dic file usually used for spellchecking to get a list of all possible words in a particular language.

you can specify your own language by just providing a specific `.dic` file, you can find them [here](https://www.phpspellcheck.com/Download)
Each one of those files ends up with some weird values at the end, this is what the `LINE_TO_STOP` const is used for.

PS: *Remember to specify the correct dict `DIC_PATH = "./dictionaries/my_dict.dic"`* you can of course use a normal`.txt` file if you prefer.
