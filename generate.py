#!/usr/bin/env python3

# Copyright 2021 https://github.com/geebee
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""generate.py - Generates diceword phrases and random passwords"""

import argparse
import gzip
import secrets
import string

from pathlib import Path


dicewords = lambda args: _dicewords(args.length, args.separator)
def _dicewords(length: int, separator: str = " ") -> str:
    if length < 1:
        raise ValueError("at least one word is required")

    word_list = dict()
    # dice-words.txt is: https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt, gzipped
    # https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
    with gzip.open(Path(__file__).resolve().parent / "dice-words.txt.gz", mode="rt") as f:
        for line in f:
            key, word = line.split("\t")
            word_list.update({key.strip(): word.strip()})

    selected_words = list()
    for _ in range(length):
        selected_words.append(
            word_list[
                "".join([str(secrets.choice([1, 2, 3, 4, 5, 6])) for _ in range(5)])
            ]
        )

    return separator.join(selected_words)


password = lambda args: _password(args.length, args.lowercase, args.uppercase, args.numbers, args.special)
def _password(
    length: int,
    lowercase: bool = True,
    uppercase: bool = True,
    numbers: bool = True,
    special: bool = True,
) -> str:
    if length < 1:
        raise ValueError("length must be at least one")

    password = list()
    sources = ""

    if lowercase:
        password.append(secrets.choice(string.ascii_lowercase))
        sources += string.ascii_lowercase
    if uppercase:
        password.append(secrets.choice(string.ascii_uppercase))
        sources += string.ascii_uppercase
    if numbers:
        password.append(secrets.choice(string.digits))
        sources += string.digits
    if special:
        password.append(secrets.choice(string.punctuation))
        sources += string.punctuation

    if len(sources) < 1:
        raise ValueError(
            "at least one of lowercase, uppercase, digits, or special must be enabled"
        )

    secrets.SystemRandom().shuffle(password)
    for i in range(length - len(password)):
        password.append(secrets.choice(sources))
        # This per character shuffling almost certainly adds nothing of value
        secrets.SystemRandom().shuffle(password)

    secrets.SystemRandom().shuffle(password)
    return "".join(password)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a diceword phrase")
    subparsers = parser.add_subparsers(required=True)

    parser_dicewords = subparsers.add_parser("dicewords")
    parser_dicewords.add_argument(
        "-le",
        "--length",
        type=int,
        default=7,
        help="number of words in the phrase",
    )
    parser_dicewords.add_argument(
        "-s",
        "--separator",
        type=str,
        default=" ",
        help="the word separator to use",
    )
    parser_dicewords.set_defaults(generator=dicewords)

    parser_password = subparsers.add_parser("password")
    parser_password.add_argument(
        "-l",
        "--length",
        type=int,
        default=32,
        help="number of characters in the password",
    )
    parser_password.add_argument(
        "--no-lowercase",
        dest="lowercase",
        default=True,
        action="store_false",
        help="do not include lower case letters in the password",
    )
    parser_password.add_argument(
        "--no-uppercase",
        dest="uppercase",
        default=True,
        action="store_false",
        help="do not include upper case letters in the password",
    )
    parser_password.add_argument(
        "--no-numbers",
        dest="numbers",
        default=True,
        action="store_false",
        help="do not include numbers in the password",
    )
    parser_password.add_argument(
        "--no-special",
        dest="special",
        default=True,
        action="store_false",
        help="do not include special characters in the password",
    )
    parser_password.set_defaults(generator=password)

    args = parser.parse_args()
    print(args.generator(args))
