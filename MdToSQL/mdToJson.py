#
# makedown表文档转表json
# #

import json
import re


# 输入json输出目录， 表脚本。输json路径
def GetJson(jsonoutpath, mdpath) -> str:
    jsonoutpath += '{}.json'

    lines = []
    with open(mdpath, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    tabDest = lines[0].replace('##', '').strip()
    tabName = lines[2].replace('>', '').strip()

    lines.pop(0)
    lines.pop(0)
    lines.pop(0)
    lines.pop(0)
    lines.pop(0)
    lines.pop(0)

    jsonlist = []
    for codeline in lines:
        if (codeline.strip() == ''):
            continue
        codeline = codeline.strip().strip('|')
        fd = codeline.split('|')

        obj = {}
        obj['name'] = fd[0].strip()
        obj['dest'] = fd[1].strip()
        obj['fdtype'] = fd[2].strip().replace(':', ',')

        if fd[3].strip() == "true":
            obj['isnull'] = True
        else:
            obj['isnull'] = False

        obj['defval'] = fd[4].strip() if fd[4].strip() != 'null' else ''

        if fd[5].strip() == "true":
            obj['ispk'] = True
        else:
            obj['ispk'] = False

        obj['forkeytab'] = fd[6].strip() if fd[6].strip() != 'null' else ''
        obj['forkeyfd'] = fd[7].strip() if fd[7].strip() != 'null' else ''
        jsonlist.append(obj)

    tab = {
        "tabName": tabName,
        "tabDest": tabDest,
        "tabFields": jsonlist
    }

    jsonstr = json.dumps(tab, ensure_ascii=False, indent=4)
    with open(jsonoutpath.format(tabName), 'w', encoding='utf8') as f:
        f.write(jsonstr)
    return jsonoutpath.format(tabName)
