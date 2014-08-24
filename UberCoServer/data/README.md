## cards.csv

Each line contains the details of one card: the first column is the ID of the
card itself, and the second column is the ID of the item the card represents.

Card IDs should be unique, but an item can have multiple cards.

## chest_keys.csv

This file lists what keys are requires to unlock each chest.

The first column is the item ID of the chest, and the second column is the item
ID of the key required to open it. If a chest requires multiple keys, it will
have one line for each key. If a chest requires multiple of the same key, just
repeat the relevant line for as many times as the number of keys of that type
are required.

## The other files

The other files are fairly straightforward and map directly to the database
schema, so view [schema.sql](schema.sql) for more information.