"""Regenerate dark_mode.svg / light_mode.svg with live GitHub stats.

Runs daily via GitHub Actions. Stdlib only, no dependencies.
"""
import calendar
import html
import json
import os
import unicodedata
import urllib.request
from datetime import datetime, timezone

USER = "yiumanlenong"
BIRTH = datetime(2002, 3, 15)
W = 56  # info column width in characters

ART = r"""

























                                                                                                                                                              ..
                                                                                                                                  ...  ....                 ..  .
                                                                                                     . ........              . ...   ...   . ...          ..  .. ...
                                                                                                      ...  ....   .         ......=*=. .=+-....... ..    .. .*##-...
                                                                                                     .. .+*. .....  .      ..... +#+%.:#*-%+ ...  . ...  . -%+.+%...    ..
                                                                                                 . ... =@+*%:... .:. ......  .. =%.-%-%=  -%:.. :=.=..... -@=  :@- ..... ..............
                                                                                                 .  . =@%#:%* ..-###= .....-=: -@: =@@- .. #* .-#-.++ ...-@= .. *#........ ....... ...
                                                                                                .....-@#.=%*%:.:@+.-#*. ...*@*=#: .=@= ....:#++*: . #-...##-: ...@- ...=%%- ....*%=   .......
                                                                                                .....%*.. :%@# =@: . +#: ..:@-#%=. .: .......:.  ...-#. .@%%%: ..=#...*@-=@= . .%#@+-+++:..  ..
                                                                                               .....##.... .*@--@-... -%- . +%#:+#+--+:..  .. ...    ::==+=.=#=   +*..+=  -%*:.=@*#@@-.    ..  .
                                                                                                .. +%....... *%+@=.....*@+..:@*  .-==-..==..   ..::*++===-.. :*#-  -:..    :%@%@@##+#@++#*-  ....
                                                                                                . =@: ......-*@@@+ .  ...**.+%%*.==.  . .#%@%+**==%#:. :#*#..  -*#-  . .:*#%**%%=*@--+=--+%*:.  ...
                                                                                           .......%= .......%#%@@%=.:+: :=%%. ..*#%= . :#+-=+#@#+*#. ...::@+...  -#*-.:#@*#%*+-. +@%*-.   :+##*-....
                                                                                      .    .  ...#* ..  . ..#-:#@%+*+-.+%-:#%: -@=#+.:+#=.    :-=-...... -%# ....  -*%@%-+%*%:  =#=@==*+=.  .:=+...
                                                                                      .    .:.. =@::.... . :#. :%@+#= -@:  .-#=@#-%#+*=. ......   ....... +@+  ....  -%%*%: *=.+#: +@: :+*+:  .. ..
                                                                                 ......... :@* :@= =*..... -%...#@:#+.#- ... :@%- #=.##.......  .:........+%#*: ......%#-   =@##=:. +@:  .-*==*#: ...
                                                                                 ....   .. +*%+%*:*+@- ....+#..#+:.%==%..... +@: :%:-@@: ... .=*=+%.      +@*@#: .....%=.-+*+++=--.. ==  :=#%%*-%- ..
                                                                              .. ... -%-...%--@*:@= %+     ## +#  .%=%= . . -@= .=% *##:... -*+: -% :=-:-+%@%:=%- ....:*++=:. .   .==:--*#=##*: -%= ..
                                                                             .... ...###..:%.+@*@%  #+ =+-=@-.@:...%@*...:.=@+ ..+#.%-#:. .*%- ..%*+*-*#=:+@#. +@=. ... .   .......:=+++**%*-. . :@- . ..
                                                                             .......+#.%: **.%#@%:.-%*#*+@+:.#+ ...@@:...*%@+ ...#=*#:@*.-=@#=+.:#*- -#.  +@: :%@#*: . ... .....  .      .=#= ... =%:....
                                                                            ...-#...#= ++=%..:#*. .@@@+. =% -%:....-:... -@- ...:%*@%-@= =#*%::+#-  :%: ..*%. *%%:%@=:*:-*: ... -+........ :@= ..==*# ...
                                                                             . +@. -%...#+...-%:...#%#+:*:***=   :#+......%+ .. +%+-%*#.....@+:%+%..#- ...%#.*%=%#@#+@@@*-#-...#%*#.        =@: -%::%: ...
                                                                             . #@:.#+ . #- . #* .. -@:*#@%:%# :+.+**#  .. +%+....--.%@-..  .*##= %**= .. :@+ -.=@%#*=%+@# =@*-.+= %+--..:=+=.%=.%=  ** ...
                                                                             ..#%-.%: . *+..:@:...-.#* +@@%%%:*@**=.%=:..==%@+ . -@-+%...=: =@@:.-*=.....=@=   :+:#@#.:@***=@#. ..:*=#@###%@:=%#@%..-@:...
                                                                            . :**=-%... =#. *#....**.@+ -@@%+##=%@: -%#= *##*@:.. +@=@:.*@#..+-.. .-..   #@:....  -=...-+-. --.  .-*#*##. *%.-@==%: .%+ ..
                                                                            . :**+*= .. :%..%= ....#+.#*.:*-.#@:=#.-=*:%=:*+=#* ...#%#+#@:@#.  . -%%= =+++-... ...  ...    .  .-+#*=: .#::@#=-*-.%*: +%...
                                                                            . -++%%:.....*-:@-. .. .#= :..   .+::#*%@+ *@=:%..%+....#%%@- -#+...-%-+*#*--%=....   ...  .:+#-...-=:   ..-#%*=@@# *@@+..%- .
                                                                            . -*=@*..  ..=##@#*+. +*:@#*: .=++. *+=%=...-. -=.:#: ...-=: . :-...%= *@+   =% ......   .-*#+-....   ......#@=%@@=-%-%@*:@- .
                                                                          ... -*:+. :**: .%#*+.*+-%@#=+##-*+:*%-#: .  ..  .  ........   ...  .... .-- ....#*-..   .=*%%@- -## .:........%@#@@*-@**#*%%*:..
                                                                        .  ....#: ..**=%:...#%--*@--:   =+-   +%+ . ...... .......   ...   .. .  ..  .....::...:=*%#+:.=###@#+*=:... ...:-=@@@@%*@=##%: ..
                                                                          ....*@#:. #= =%: +@##@%=*+ ...   ... .....          ...              ... .. .  .. ..-#+=:   . .: :-==++-...... :%@@##%#%@%-@-..
                                                                        .  ...:*+++-%-. *%:%@@#@+ ...   ...   .  .                                        ......  .... . ..:=*+:...   .. +@@@-#@=#+::@: .
                                                                        .  ... .  :+=. ..*@@#-:= .  .      ..  .                                            . .......  ....*%..=  .:-+: +@*%@#@%#%=**@: ..
                                                                            ....-.  =%+...==.   ..  .                                                                   ....+#=%*+*+=::#*+@@#%@@*%+%@#....
                                                                            ....#--:*#*+..   ......                                                                     .... -#+::. ..*#-*+#+@@+-#@@%= ...
                                                                             .. *+-=*@+...... ..                                                                        .  .. .**...-%*.-:-@@%@%++@-#- ...
                                                                             .. +* . :##:..                                                                                .... +#. +%:.:*@@+#%--@#*%.....
                                                                             .. :#-@= .#-...                                                                               ..... =#=%@#*%%*@@+.-@@%@+ ...
                                                                            . ...+**+*:%:..                                                                                  .... *@**%-.:+@#..#@%*%...
                                                                              .. -@*+*:%: .                                                                     .....        ...*:.%#@@@@%@@@-*@@#%= .
                                                                               ...+%##:%: ..        .                                                     . ....     ...   .....#@:#-=@#@%%#%@%@@@#...
                                                                                 . *+%#%....      ..  .                                                  . .  ..:+==-  ...  ....:%@%- =%%@#%+.:@@@: ..
                                                                                 ..-%+=@= ..     .  ......  ..                                           .. .: .%@==%#- ..... ...:*@- .%@@@# .*@@* ...
                                                                                 ...*@-%#.........:*#... ........ ..                             ......... =*@*:-*#*.=#+. ... ...  -%-.=%@-.=*#@%....
                                                                                 ....+@*#= ....  .#@#=..:..  .   .   .                      .....        .-#+-@@*#**%*:+#=. ..  ... -%- :#**+.+%:.......
                                                                                 .... +%@#..  .-+@@*+*-*= -*:::.. :.. ..    .  ...      . .. .  ..=+-*+:+##*%.-@@+@==@@-:#%=...  ...=#+:.==#:.@-        ..
                                                                                    ...#**:.-=+%@=+@*+%==+%@@@@%+-%: +* ......   .       ...:::::#@@@%+%##= .. :: .. :%@+.+#...  ...*+=-.%=:.*#.:--====:..
                                                                                    .. -#+=:--*#+ =-+@#*%@@%@%=-%%-:**+-......   .     .. .:##*#+-*%=+.::... ..  .  . .:+- ..    ...%%%%=.%%+#@%+=:.::==..
                                                                                 .. ....#%...*- .. :#-=-...-*: =+..*- ..=#-...        ...:. -#%=*- :. .  . ............   . . .. ...*:***#%*@%%@%%*-.  ...
                                                                                  ..  ...*+ :. ......   ... ........ ....-...         ...=+++-:....  .....     ..      .-:::.... .... +@%@%#=#@*=+-#%#=...
                                                                                       . .%- .... ..   ........... .. ..    ..        ... ..   ......    .:--+##%*+=**+*%#+++=.... ...:%@@=+:*=:   .*%+..
                                                                                      ... :%:.. .-..:-=-          .....  ...  .          .  ... .   ..:=++++*#@@@@*#%-::.   ...... .. =#**= .. .... -@=*: .
                                                                                      ...---#.-#%@%+*@%#***++:....      ...... ...      .........=**+==--.-*%@@@@@@%: . .......... ...:-#:.=: .. ....%=*- .
                                                                                      ...:%:#+.:--:. ++::+@@@@%*+#+=--:.....:%=...          ....++-:.     :##%@@@@%=.... ....      ....+= :=:...... .#-*: .
                                                                                      .. :#%-%:    .. .. :@#%@@@+*=:-==..... :#:..          .....   ........ -##*=:.......   ...     ..  .   .... :*#**+ .
                                                                                      ..-@@@+*+....... ...=*%@@%#%:     . . . ..             ... ...      ......   . .. ..:-:...     ........... -%@@*+...
                                                                                      . +@%@%## ... .. ... =++%@@=.....      .                               .  ...    ...#@+ ..           .....+@@##= ...
                                                                                      ..:%:#%@@-:....  ....-++***:...  .      .  .                        .   .        ....:....           ....#@@@=. ....
                                                                                      .. **:#%@@+ ...     ...     ...        ..-. .                                      .            . .... :%@%%= .. .
                                                                                      ...-@**%@*.....    .. ........        ..:%...                                     . ...         .... .=@@**- ...  .
                                                                                      ....*@#*@* ....         . .           ..+# .                                               ......  .:*@%: . ..
                                                                                      .....-%*+@:....                     ... #* .                                                ..   -:.+@+. ....
                                                                                      ..... .#*#%....                   .... -@:..                                              .....+#%#=+- ...
                                                                                          ....%+%= ..                     ...#* ..                                             ....=*=:::.  ..
                                                                                          ... -=-%:..                    .. :@-..        ..                                    ...*-.    ... ...
                                                                                            ..   +# .                   ... +%...     .... .                                  ...-%...+*....
                                                                                           .  ....#: .                  ....%+ ...    .. .....                               ... *=  +%:...
                                                                                           .    . +# .....              ....+%-...    ..:#:...                               .. :#.. #* ...
                                                                                                ...#+ ....              .... -*+..    ..-= ..  .                            ... #+ . #*.. .
                                                                                                ....%- ..              ....-+: ...    ... .   ..                             . -%... ## ...
                                                                                                . . -%: ...             ....:.....      ...                                 ...%- .. *#....
                                                                                                . .. +#....              ...                                               ...#+ ... +@.....
                                                                                                 .... %+ ..  .             .............. . .  .                        .....*#..... -@: ..
                                                                                                    ..:%: . ..               .         .........                       .....#*... .. :@= .
                                                                                                    .. =%. ...              ....:::-=++++++=....                      .....#* .... ...%# ...
                                                                                                     .. +%: ...             ...=+++=-::.......                     ....  .%@..... ... *%...
                                                                                                     ... =%- ..             ....     .::...                       ..   :+%@=....  ... =@: .
                                                                                                     . .. :@+. ....    .     ........+*=....  ..               ...  :=+%@*. .     . . :@- ..
                                                                                                         . :%%-   .. ..            ..                       ..... :**##=. ...       . .%* .
                                                                                                          . :-+*-: .. .           ....... .               ..... .+#==+: .....        . +@...
                                                                                                          ..   -#@- ....                                  ... .=@@- :. ....        . . -@:..  .
                                                                                                           .... .-#*. ...                               ...  =%@*:.. ..            . ...@+ ..
                                                                                                              ... .+#=.  ...                    ... ...   :=#%*: .. .      ..      . .. +@:..
                                                                                                                ... :+#+:.  ..                 ......  .=*#*-.  ....                 ....%+ ...
                                                                                                                 .... .=**=.  ...  .  .. ...... .   :=*#*=:  .....                .. ... =@:.. .
                                                                                                                   ...  .:+#+... .....         ..:=***=:   ...   .                    ....%* ...
                                                                                                                      ...  .+-..:. .  :..::::-:.=+=-.   ...                            ...-%: ..
                                                                                                                     . ..... ...+*=###@##***%+:..   .... .                              .. =%:    ..
                                                                                                                           ......---=+==-+%+:. ......                                   ... =*+.....
                                                                                                                            .....      . ##. ....   .                                    ... .=:...
                                                                                                                             .   .......-%:... .                                           ..   ..
                                                                                                                                      .=*- ... .                                             ...
                                                                                                                                      ..  .    .
                                                                                                                                        ..

























"""

# Two tokens by design:
#   GITHUB_TOKEN - built-in Actions token, scoped to THIS repo only; it cannot see
#                 the user's other private repos, so it only yields public data.
#   ACCESS_TOKEN - PAT (repo scope) from the secret; required to read private repos
#                 (repo list + LOC walk) AND to count private contributions.
# PRIV_TOKEN prefers ACCESS_TOKEN; TOKEN falls back to GITHUB_TOKEN when no PAT is set.
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("ACCESS_TOKEN") or ""
PRIV_TOKEN = os.environ.get("ACCESS_TOKEN") or TOKEN


def gh(url, payload=None, token=None):
    headers = {"Accept": "application/vnd.github+json"}
    if token or TOKEN:
        headers["Authorization"] = f"Bearer {token or TOKEN}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode() if payload else None,
        headers=headers,
    )
    with urllib.request.urlopen(req) as r:
        return r.status, json.loads(r.read() or "{}")


def graphql(query, variables=None, token=None):
    _, resp = gh("https://api.github.com/graphql", {"query": query, "variables": variables or {}}, token)
    if resp.get("errors"):
        raise RuntimeError(resp["errors"])
    return resp["data"]


def created_at():
    data = graphql(f'query {{ user(login: "{USER}") {{ createdAt }} }}')["user"]
    return datetime.fromisoformat(data["createdAt"].replace("Z", "+00:00"))


def age(b, t):
    years = t.year - b.year - ((t.month, t.day) < (b.month, b.day))
    months = (t.month - b.month - (t.day < b.day)) % 12
    if t.day >= b.day:
        days = t.day - b.day
    else:
        pm_year, pm = (t.year, t.month - 1) if t.month > 1 else (t.year - 1, 12)
        days = calendar.monthrange(pm_year, pm)[1] - b.day + t.day
    return years, months, days


def fetch_stats():
    joined = created_at()
    joined_year = joined.year
    now_year = datetime.now(timezone.utc).year
    yr_aliases = "\n".join(
        f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y + 1}-01-01T00:00:00Z")'
        " { totalCommitContributions restrictedContributionsCount }"
        for y in range(joined_year, now_year + 1)
    )
    contrib = graphql(f'query {{ user(login: "{USER}") {{ {yr_aliases} }} }}', token=PRIV_TOKEN)["user"]
    commits = sum(
        v["totalCommitContributions"] + v["restrictedContributionsCount"]
        for v in contrib.values()
    )
    u = graphql(f"""
    query {{
      user(login: "{USER}") {{
        id
        followers {{ totalCount }}
        repositories(first: 100, ownerAffiliations: OWNER) {{
          totalCount
          nodes {{ name stargazerCount isFork }}
        }}
        repositoriesContributedTo(first: 1, contributionTypes: [COMMIT, PULL_REQUEST, REPOSITORY]) {{
          totalCount
        }}
      }}
    }}""", token=PRIV_TOKEN)["user"]
    stats = {
        "followers": u["followers"]["totalCount"],
        "repos": u["repositories"]["totalCount"],
        "contributed": u["repositoriesContributedTo"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "commits": commits,
        "joined": joined,
    }
    stats.update(loc([n["name"] for n in u["repositories"]["nodes"] if not n["isFork"]], u["id"]))
    return stats


LOC_QUERY = """
query($owner: String!, $name: String!, $id: ID!, $cursor: String) {
  repository(owner: $owner, name: $name) {
    defaultBranchRef { target { ... on Commit {
      history(first: 100, author: {id: $id}, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes { additions deletions }
      }
    } } }
  }
}"""


def loc(repo_names, user_id):
    # REST stats/contributors answers 202 forever to the Actions token,
    # so walk own commits on the default branch via GraphQL instead.
    add = rem = 0
    for name in repo_names:
        cursor = None
        try:
            while True:
                ref = graphql(LOC_QUERY, {"owner": USER, "name": name, "id": user_id, "cursor": cursor}, token=PRIV_TOKEN)["repository"]["defaultBranchRef"]
                if ref is None:
                    break  # empty repo
                h = ref["target"]["history"]
                add += sum(n["additions"] for n in h["nodes"])
                rem += sum(n["deletions"] for n in h["nodes"])
                if not h["pageInfo"]["hasNextPage"]:
                    break
                cursor = h["pageInfo"]["endCursor"]
        except Exception as e:
            print(f"loc {name}: {e}")
    return {"loc_add": add, "loc_del": rem, "loc": add - rem}


def disp_width(s):
    # East-Asian chars render ~2 cells wide in a monospace font; count them as 2
    # so the dotted leaders line up even when the value contains Chinese text.
    return sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in s)


PALETTES = {
    "dark": {"bg": "#0d1117", "border": "#30363d", "art": "#8b949e", "h": "#58a6ff",
             "k": "#ffa657", "v": "#c9d1d9", "d": "#484f58", "g": "#3fb950", "r": "#f85149"},
    "light": {"bg": "#ffffff", "border": "#d0d7de", "art": "#57606a", "h": "#0969da",
              "k": "#953800", "v": "#24292f", "d": "#afb8c1", "g": "#1a7f37", "r": "#cf222e"},
}


def kv(key, val, width=W):
    dots = "." * max(width - disp_width(key) - disp_width(str(val)) - 3, 1)
    return [(f"{key}: ", "k"), (dots + " ", "d"), (str(val), "v")]


def kv2(k1, v1, k2, v2):
    left = kv(k1, v1, 30)
    return left + [(" | ", "d")] + kv(k2, v2, 23)


def rule(title=""):
    label = f"─ {title} " if title else ""
    return [(label, "h"), ("─" * max(W - disp_width(label), 1), "d")]


def info_lines(s):
    by, bm, bd = age(BIRTH, datetime.now(timezone.utc))
    n = lambda x: f"{x:,}"
    return [
        [(f"{USER.lower()}@github ", "h"), ("─" * (W - len(USER) - 8), "d")],
        [],
        kv("OS", "Windows"),
        kv("Age", f"{by} years, {bm} months, {bd} days"),
        kv("Host", "Shenzhen Jumper Medical Equipment Co.,Ltd"),
        kv("Kernel", "Embedded Firmware Engineer"),
        kv("IDE", "VS Code / CodeBuddy"),
        [],
        kv("Languages.Programming", "C"),
        kv("Languages.Real", "Chinese, English"),
        kv("Hobbies", "Running Cycling Coffee"),
        [],
        rule("Contact"),
        kv("Email", "yiumanlenong@qq.com"),
        kv("LinkedIn", "in/yiuman-lenong-a074612b5"),
        [],
        rule("GitHub Stats"),
        kv2("Repos", f"{s['repos']} {{Contributed: {s['contributed']}}}", "Stars", n(s["stars"])),
        kv2("Commits", n(s["commits"]), "Followers", n(s["followers"])),
        [("Lines of Code: ", "k"), (n(s["loc"]), "v"), (" ( ", "d"),
         (n(s["loc_add"]) + "++", "g"), (", ", "d"), (n(s["loc_del"]) + "--", "r"), (" )", "d")],
    ]


def render(mode, stats):
    p = PALETTES[mode]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="560" viewBox="0 0 1040 560" '
        f'font-family="Consolas, Menlo, monospace" font-size="13px">',
        f'<rect x="0.5" y="0.5" width="1039" height="559" rx="10" fill="{p["bg"]}" stroke="{p["border"]}"/>',
    ]
    for i, line in enumerate(ART.strip("\n").split("\n")):
        out.append(f'<text x="25" y="{45 + i * 4}" fill="{p["art"]}" font-size="3.5" xml:space="preserve">{html.escape(line)}</text>')
    for i, segs in enumerate(info_lines(stats)):
        if not segs:
            continue
        spans = "".join(f'<tspan fill="{p[c]}">{html.escape(t)}</tspan>' for t, c in segs)
        out.append(f'<text x="545" y="{45 + i * 21}" xml:space="preserve">{spans}</text>')
    out.append("</svg>")
    return "\n".join(out)


def selfcheck():
    assert age(datetime(2023, 1, 29), datetime(2026, 8, 24)) == (3, 6, 26)
    assert age(datetime(2000, 3, 31), datetime(2026, 4, 1)) == (26, 0, 1)
    assert age(datetime(2000, 1, 1), datetime(2026, 1, 1)) == (26, 0, 0)
    assert disp_width("中文English") == 11  # 2 CJK (×2) + 7 ASCII = 11


if __name__ == "__main__":
    selfcheck()
    stats = fetch_stats()
    print("stats:", stats)
    for mode in PALETTES:
        with open(f"{mode}_mode.svg", "w", encoding="utf-8") as f:
            f.write(render(mode, stats))
    print("wrote dark_mode.svg, light_mode.svg")
