import json

t = open("wikicountries.txt").read()
d = {}
f = open("wikicountries.json", "w")

#import pdb; pdb.set_trace()
while True:
    idx = t.find("ISO 3166-1 alpha-2")
    if idx == -1:
        break
    code2 = t[idx+24: idx+26]
    code3 = t[idx+24+26: idx+26+27]
    d[code3] = {'code2': code2}
    previdx = t[:idx].rfind("href")
    hrefidx = t[:previdx - 4].rfind("href")
    idx1 = t[hrefidx:].find('"')
    idx2 = t[hrefidx + idx1 + 1:].find('"')
    d[code3]["url"] = "https://en.wikipedia.org" + t[hrefidx + idx1 + 1: hrefidx+ idx1 + idx2 + 1]
    t = t[idx+26:]

f.write(json.dumps(d))
f.close()
