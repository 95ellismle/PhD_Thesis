from collections import Counter, OrderedDict
import os
import re
from typing import List
from nltk import pos_tag


folder = '../'


class TexFile:
    def __init__(self, filepath):
        self.filepath = filepath

        self.ftxt = self._load_file_(filepath)
        self.text_data = self._get_real_txt_(self.ftxt)

    def _load_file_(self, filepath: str) -> str:
        """Read the filetxt and return it"""
        with open(filepath, 'r') as f:
            return f.read()

    def _get_real_txt_(self, ftxt: str) -> dict:
        """Will get the actual text from a file without LaTeX commands

        Args:
            ftxt: the file text

        Returns:
            dictionary with text decomposed by command (e.g. real, math)
        """
        txt, env_txt = self._rm_envs_(ftxt)
        txt, comments = self._rm_comments_(txt)
        txt, comments = self._rm_cmds_(txt)

        txt = txt.replace('}', '')
        txt = txt.replace('\\\\', '\n')
        txt = re.sub('\\\\[a-zA-Z_]+ ', '', txt)
        return txt

    def _rm_comments_(self, txt):
        """Remove comments in the text"""
        all_occ = self._get_env_helper_(txt, '%', '\n')

        # Remove esacped % signs
        occ = {f'\\{i}': i for i in all_occ}
        occEscaped = self._get_env_helper_(txt, '\\%', '\n')
        occToRemove = {occ[i]: all_occ[occ[i]] for i in occ if i not in occEscaped}

        txt = self.__rm_from_txt__(txt, occToRemove)

        return txt, occToRemove

    def _rm_cmds_(self, txt):
        """Will remove any commands (\command{...})"""
        cmds = set(re.findall('\\\[a-zA-Z_-]*{', txt))

        rm_cmd_names = ('eqref', 'cite', 'ref', 'label')
        rm_cmd_names = [f'\\{i}'+'{' for i in rm_cmd_names]
        tmp = set(rm_cmd_names)
        for i in tmp:
            if i in cmds: cmds.remove(i)
            else:         rm_cmd_names.remove(i)
        rm_full_cmd = rm_cmd_names

        all_envs = {}
        for i in rm_full_cmd:
            envs = self._get_env_helper_(txt, i, '}')
            txt = self.__rm_from_txt__(txt, envs)
            all_envs.update(envs)

        all_envs = {}
        for i in cmds:
            envs = self._get_env_helper_(txt, i, '')
            txt = self.__rm_from_txt__(txt, envs)
            all_envs.update(envs)

        return txt, all_envs

    def _get_env_helper_(self, txt: str, start_str: str, end_str: str) -> List[str]:
        """A helper to find env expressions because I can't do RegEx.

        Will find things like the '\gamma' in "bob $\gamma$ bob" and
        return '\gamma' and the indices.
        """
        i=0
        occurances = {}
        ls, le = len(start_str), len(end_str)
        c = 0

        while txt.find(start_str) != -1:
            i+= 1
            start_ind = txt.find(start_str)
            txt = txt[start_ind+ls:]

            end_ind = txt.find(end_str)
            if end_ind != -1:
                key = f'{start_str}{txt[:end_ind]}{end_str}'
                occurances.setdefault(key, []).append((start_ind + c,
                                                       start_ind + end_ind + le + c + ls))

                txt = txt[end_ind+le:]
                c += start_ind + end_ind + le + ls

            else:
                break

        return occurances

    def __rm_from_txt__(self, txt, inds):
        """Will remove a dictionary of indices from a string"""
        inds = {j: i for i in inds for j in inds[i]}

        count = 0
        for i in sorted(inds):
            diff = i[1] - i[0]

            assert txt[i[0]-count:i[1]-count] == inds[i]
            txt = txt[:i[0]-count] + txt[i[1]-count:]

            count += diff

        return txt


    def _rm_envs_(self, txt: str) -> str:
        """Separate math commands and everything else."""
        all_env = {}

        env_occ = self._get_env_helper_(txt, '$', '$')
        txt = self.__rm_from_txt__(txt, env_occ)
        all_env.update(env_occ)

        env_occ = self._get_env_helper_(txt, '\\[', '\\]')
        txt = self.__rm_from_txt__(txt, env_occ)
        all_env.update(env_occ)

        env_occ = self._get_env_helper_(txt, '\\(', '\\)')
        txt = self.__rm_from_txt__(txt, env_occ)
        all_env.update(env_occ)

        for env in ('figure', 'split', 'table', 'center', 'align', 'equation',
                    'itemize', 'minipage', 'wrapfigure', 'enumerate', 'tabular',
                    'dmath', 'equation*', 'flalign*', 'array', 'align*'):

            env_occ = self._get_env_helper_(txt,
                                            '\\begin{%s}' % env,
                                            '\\end{%s}' % env)
            txt = self.__rm_from_txt__(txt, env_occ)
            all_env.update(env_occ)

        return txt, all_env



txt = ""
for fn in os.listdir(folder):
    if not fn.endswith('.tex'):
        continue

    file_data = TexFile(f'{folder}/{fn}')
    txt += file_data.text_data


def sort_counts(cnts):
    """Will return a sorted dict of cnts sorted by count"""
    items = [(cnts[i], i) for i in cnts]
    items.sort()

    ret_dict = OrderedDict()
    for i, key in items[::-1]:
        ret_dict[key] = i

    return ret_dict


def clean_words(words):
    """remove commas, punctuation etc from words"""
    words = [i for i in words if not any(j in i for j in '_0123456789{}[]/=@\\')]
    new_words = []
    for i in words:
        wrd = i[:]
        for i in '().,:!?;`"':
            wrd = wrd.replace(i, '')

        wrd = wrd.strip('-').lower()

        if len(wrd):
            new_words.append(wrd)

    return new_words


def get_word_hist(word_counts):
    """Get the histogram of lengths of words"""
    all_len = {}
    for i in word_counts:
        l = len(i)
        all_len.setdefault(l, 0)
        all_len[l] += word_counts[i]

    return all_len


def get_word_lens(word_counts):
    """Create sorted dict for each word len"""
    all_lens = {}
    for i in word_counts:
        all_lens.setdefault(len(i), {})
        all_lens[len(i)][i] = word_counts[i]

    all_lens = {i: sort_counts(all_lens[i]) for i in all_lens}
    return all_lens


def is_ok_word(word):
    """Will check if the word is ok for the word cloud"""
    PT = pos_tag([word])
    bad_wrd_types = {'DT', 'CC', 'MD', 'IN', 'VBZ', 'DT', 'IN',
                     'PRP', 'TO', 'VBN', 'RB', 'RBR', 'CD',
                     'VBP', 'VBD', 'VB', 'PRP$', 'WDT', 'WRB',
                    }
    if PT[0][1] in bad_wrd_types:
        return False
    return True


def get_top_words(sorted_words, n_words=200):
    """Get the most frequent OK words"""
    top_words = []
    count = 0
    for wrd in sorted_words:
        if count >= n_words: break

        elif is_ok_word(wrd):
            elm = (wrd, sorted_words[wrd])

            top_words.append(elm)
            count += 1

    max_wrd_usage = top_words[0][1]
    top_words = [(i, j/max_wrd_usage) for i, j in top_words]
    return top_words


def write_csv(top_words, fn='top_words.csv'):
    """Will write the top_words as a csv"""
    with open(fn, 'w') as f:
        txt = 'word,freq\n'
        main_data = '\n'.join(map(lambda row: ','.join(map(str, row)), top_words))
        f.write(txt + main_data)



letter_counts = Counter(txt.lower())
sorted_letters = sort_counts(letter_counts)

words = clean_words(txt.split())
word_counts = Counter(words)
sorted_words = sort_counts(word_counts)
word_lens = get_word_lens(sorted_words)
word_hist = get_word_hist(word_counts)
top_words = get_top_words(sorted_words, 1000)
write_csv(top_words)

