
### constants used in base/messenger.py ###

# Establishes what methods messengers are allowed to call
# Tipically, this should only be the ones established in the protocol
ALLOWED_METHODS = ['sync']

# Establishes the max size of each chunk read by a reading messenger.
# Generally a small power of 2 (8192, 4096)
CHUNK_SIZE = 256

# Separator of multiple messages during same transmission in a messenger.
# Should be something you definetely won't find inside another message.
SEPARATOR = '\n<separator>\n'
