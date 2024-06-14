# bencoding

`bencoding` is a simple Python library for decoding bencoded data.

```python
import bencoding

data = bencoding.decode(b'li1ei2ei3ee')
print(data) # [1, 2, 3]

data = bencoding.decode(b'd3:foo3:bare')
print(data) # {'foo': 'bar'}

data = bencoding.decode(b'i42e')
print(data) # 42

data = bencoding.decode(b'4:spam')  
print(data) # b'spam'

my_torrent = pathlib.Path('my_torrent.torrent')
my_torrent_bytes = my_torrent.read_bytes()
data = bencoding.decode(my_torrent_bytes)
print(data)
```