import os, re

all_envs = set()
for fn in os.listdir('../Revised_postViva'):
    if not fn.endswith('.tex'): continue

    with open(f'../Revised_postViva/{fn}', 'r') as f:
            txt = f.read()

    for i in re.findall('begin *{.*}', txt):
        all_envs.add(i[i.find('{')+1:i.find('}')])

print(all_envs)
