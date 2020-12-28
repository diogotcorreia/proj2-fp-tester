posicaoMocks = (
    lambda c, l: {n: 'c' if chr(n) == c else 'l' if chr(n) == l
                  else '' for n in range(122, -1, -1)},
    lambda p: {k: v for (k, v) in p.items()},
    lambda p: chr([k for (k, v) in p.items() if v == 'c'][0]),
    lambda p: chr([k for (k, v) in p.items() if v == 'l'][0]),
    lambda p: type(p) == dict and [*p.keys()] == [*range(123)] and
    [*p.values()].count('c') == [*p.values()].count('l') == 1,
    lambda p1, p2: type(p1) == type(p2) == dict and
    [*p1.keys()] == [*p2.keys()] == [*range(123)] and
    [*p1.values(), *p2.values()].count('c') ==
    [*p1.values(), *p2.values()].count('l') == 2 and
    [*p1.values()].index('c') == [*p2.values()].index('c') and
    [*p1.values()].index('l') == [*p2.values()].index('l'),
    lambda p: ''.join([chr(k)
                       for (k, v) in p.items() if v in ('c', 'l')][::-1])
)

pecaMocks = (
    lambda s: {'foo': 'bar'.join([chr(n) for n in range(ord(s))])},
    lambda j: {'foo': j['foo']},
    lambda j: j in tuple({'foo': 'bar'.join([chr(n) for n in range(m)])}
                         for m in (32, 88, 79)),
    lambda j1, j2: all(j in tuple({'foo': 'bar'.join(
        [chr(n) for n in range(m)])} for m in (32, 88, 79))
        for j in (j1, j2)) and len(j1['foo']) == len(j2['foo']),
    lambda j: ''.join(
        [chr(n) if n != 92 else chr(ord(j['foo'][-1]) + 1) for n in range(91, 94)])
)
