## Generate Passwords

A Python 3+, stdlib only, secure (via use of the `secrets` module for randomness) dicewords phrase or password generator.

### Diceword Phrase

The word list for diceword phrases comes from the [EFF](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases).

To generate a diceword phrase, run: `./generate.py dicewords`
  - The default number of words in a phrase is 7, but any number (>=1) can be set with the `--words` (`-w`) flag
  - The default separator between words is `" "` (a space), but any separator can be set with the `--separator` (`-s`) flag

### Password

To generate a password, run: `./generate.py password`
  - The default length of the password is 32, but any length (>=1) can be set with the `--length` (`-l`) flag
  - The default character set for passwords is all (ASCII printable) letters (upper and lower cases), numbers, and special characters (punctuation)
    - Lower case letters can be excluded from the generated password with the `--no-lowercase` flag
    - Upper case letters can be excluded from the generated password with the `--no-uppercase` flag
    - Numbers can be excluded from the generated password with the `--no-numbers` flag
    - Special characters can be excluded from the generated password with the `--no-special` flag

**NOTE:** Generated passwords are guarantueed to have at least one of each enabled character class in the final password.
