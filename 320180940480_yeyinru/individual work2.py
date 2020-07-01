from subprocess import Popen, PIPE
import re,time,unicodedata
import pandas as pd

def git_run(cmd):
    p = Popen(cmd, cwd=repo, stdout=PIPE)
    data, res = p.communicate()
    data = unicodedata.normalize(u'NFKD', data.decode(encoding="utf-8", errors="ignore"))
    return data
	
repo = "./linux-stable"
kernelRange = "v4.1..v4.1.3"

cmd = ["git", "log", "--pretty=format:%h %ad", "--date=raw", kernelRange]
data = git_run(cmd)

df = pd.DataFrame(columns = ['hash', 'time'])
for line in data.split("\n"):
    Hash, seconds, time_zone = line.split()
    if time_zone[0] == "+":
        seconds = int(seconds) + (int(time_zone[2])*3600 + int(time_zone[3])*600)
    else:
        seconds = int(seconds) - (int(time_zone[2])*3600 + int(time_zone[3])*600)
    df.loc[df.shape[0]] = [Hash, seconds]

df = df.sort_values(by='time')
fin = pd.DataFrame(columns = ['hash', 'Time since last submission'])
fin['hash'] = df['hash']
tmpa = df['time'].append(df['time'].tail(1))
tmpa.index = range(tmpa.shape[0])
tmpb = df['time'].head(1).append(df['time'])
tmpb.index = range(tmpb.shape[0])
tmp = tmpa - tmpb
tmp = tmp[:138]
fin.index = range(fin.shape[0])
fin['Time since last submission'] = tmp
fin.to_csv("work2.csv")