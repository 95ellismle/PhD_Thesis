import re, os, shutil

files = {'Appendices.tex', 'Chapter3_orig.tex', 'MainPackages.tex', 'Chapter5.tex', 'Preamble.tex',
         'CTMQC_Applied_To_Tully_Models.tex', 'Chapter5_ChargeTrans.tex', 'Introduction.tex', 'outlook.tex',
         'Chapter5_MD.tex', 'Chapter3.tex', 'Chapter6.tex', 'Main.tex'}

folder = 'Revised_postViva'
new_folder = 'FinalPDFs'

if os.path.isdir(new_folder):
    shutil.rmtree(new_folder)
os.makedirs(new_folder)

all_files = os.listdir(folder)
files_to_copy = set(all_files).difference(files)


def get_matched_braces(txt, s_ind):
    """Will get the point at which a brace closes.
    """
    vals = {'{': 1, '}': -1}
    cond = 1
    adder = txt[s_ind:].find('{')
    if adder == -1: return -1, -1

    e_ind = s_ind + adder + 1
    while cond != 0 and e_ind < len(txt):
        s = txt[e_ind]
        cond += vals.get(s, 0)

        e_ind += 1
    return e_ind


def search_for_env_via_desc(txt, env_desc):
    """Will search for a particular environment and return the index of the occurance

    Args
        txt:      the file text
        env_desc: what to look for

    Returns
        a list of occurances of the envs and the text
    """
    start_str = env_desc['start']

    if env_desc.get('do_regex') is True:
        s_ind = re.search(start_str, txt)
        if s_ind is None: return -1, -1
        s_ind = s_ind.start()
    else:
        s_ind = txt.find(start_str)

    if s_ind == -1:
        return -1, -1

    # Return matched braces
    if env_desc.get('count_braces'):
        e_ind = get_matched_braces(txt, s_ind)

    # Don't count braces
    else:
        e_ind = txt[s_ind:].find(env_desc['end'])
        if e_ind == -1: return -1, -1
        e_ind += s_ind

    return s_ind, e_ind


def get_all_envs(txt, env_desc):
    """Will get the environments to remove etc..

    Args
        txt:      the file text
        env_desc: what to look for

    Returns
        a list of occurances of the envs and the text
    """
    all_envs = []

    start_ind, end_ind = search_for_env_via_desc(txt, env_desc)
    cum_i = 0
    while start_ind != -1:
        start_ind, end_ind = search_for_env_via_desc(txt, env_desc)
        if start_ind == end_ind: continue
        all_envs.append((start_ind+cum_i,
                         end_ind+cum_i,
                         txt[start_ind:end_ind]))

        txt = txt[end_ind:]
        cum_i = end_ind

    return all_envs




bad_ext = ('.pdf', '.log', '.py', '.lof', '.lot', '.toc', '_orig.tex', '_ORIG.tex', '.aux')
for fn in all_files:
    fp = f'{folder}/{fn}'
    if os.path.isdir(fp): continue

    if any(fn.endswith(j) for j in bad_ext):
        continue

    new_fp = f'{new_folder}/{fn}'

    if fn in files:
        with open(fp, 'r') as f:
            txt = f.read()

        # Handle removes
        all_remove_envs = get_all_envs(txt, {'start': '\\\\[m]*remove *(\[[a-zA-Z]*\])*{',
                                             'count_braces': True,
                                             'do_regex': True})
        for i in all_remove_envs:
            txt = txt.replace(i[2], '')

        # Handle adds
        all_add_envs = get_all_envs(txt, {'start': '\\\\[m]*add *{',
                                          'count_braces': True,
                                          'do_regex': True})
        for i in all_add_envs:
            new_str = i[2][i[2].find('{')+1:-1]
            txt = txt.replace(i[2], new_str)

        # Handle replacements
        all_replace_envs = get_all_envs(txt, {'start': '\\\\[m]*replace *{',
                                              'count_braces': True,
                                              'do_regex': True})
        for i in all_replace_envs:
            s_ind = txt.find(i[2])
            del_str = txt[s_ind:s_ind + len(i[2])]
            add_str_start = txt[s_ind + len(i[2]):].find('{')
            new_s_ind = s_ind + len(i[2]) + add_str_start
            brace_close_txt = txt[new_s_ind:]
            e_ind = get_matched_braces(brace_close_txt, 0) + new_s_ind
            new_str = txt[new_s_ind:e_ind]
            assert new_str.startswith('{')
            assert new_str.endswith('}')
            del_str = del_str + new_str
            new_str = new_str[1:-1]
            assert del_str in txt
            assert 'replace' in del_str
            assert new_str in del_str
            txt = txt.replace(del_str, new_str, 1)

        # Now save the final tex files
        with open(new_fp, 'w') as f:
            f.write(txt)

    else:
        shutil.copyfile(fp, new_fp)
