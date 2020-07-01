from subprocess import Popen, PIPE
import re,time,unicodedata

def git_run(cmd):
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
    return data
	
repo = "E:\pythonTest\linux-stable\linux-stable"
kernelRange = "v4.0..head"

cmd = ["git", "log", "--oneline", "--no-merges", kernelRange]
data = git_run(cmd)

import pandas as pd
df = pd.DataFrame(columns = ['hash','version','time'])
commit = re.compile('.{12} Linux [4-5]\.[0-9]{1,2}$')
for line in data.split("\n"):
    if commit.match(line):
        Hash, version = line.split(" ", 1)
        cmd = ["git", "show", "{}".format(Hash), "--pretty=format:%ad", "--date=iso"]
        inf = git_run(cmd).split("\n")[:1][0]
        df.loc[df.shape[0]] = [Hash, version, inf]
print(df)
df.to_csv("idw.csv")