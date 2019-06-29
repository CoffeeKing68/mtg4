import re

class Rules():
    def __init__(self, string):
        self.string = string
        self.paragraphs = []
        for paragraph in string.splitlines():
            self.paragraphs.append(Paragraph(paragraph))

    def __str__(self):
        return "Rules:\n" + "\n".join([f" {i} {p.__str__()}" for i, p in enumerate(self.paragraphs)])

class Paragraph():
    pmana = re.compile("{.+?}")
    pital = re.compile("<i>")
    pitalend = re.compile("<\/i>")

    def __str__(self):
        return "Paragraph:\n" + "\n".join([f"  {i} {w}" for i, w in enumerate(self.words)])

    def __init__(self, string):
        self.string = string

        t = string
        ital = False
        self.words = []
        for t in string.split(" "):
            w = []
            while len(t) > 0:
                mmana = Paragraph.pmana.search(t)
                mital = Paragraph.pital.search(t)
                mitalend = Paragraph.pitalend.search(t)

                matches = sorted([mmana, mital, mitalend], key=lambda m: len(t) + 1 if m is None else m.start())
                match = matches[0]

                if match is None:
                    w.append(ItalicsText(t) if ital else Text(t))
                    t = ""
                else:
                    if match.start() > 0:
                        w.append(ItalicsText(t[:match.start()]) if ital else Text(t[:match.start()]))

                    if match.group()[0] == "{": # Mana
                        w.append(ManaText(t[match.start():match.end()]))
                        t = t[match.end():]
                    elif match.group() == "<i>":
                        match1 = matches[1]
                        if match1 is None:
                            w.append(ItalicsText(t[match.end():]))
                            ital = True
                            t = ""
                        else:
                            w.append(ItalicsText(t[match.end():match1.start()]))
                            if match1.group() == "</i>":
                                t = t[match1.end():]
                            else:
                                t = match1.group() + "<i>" + t[match1.end():]
                    elif match.group() == "</i>":
                        t = t[match.end():]
                        ital = False

            self.words.append(w)

class Text():
    def __init__(self, string):
        self.string = string

    def getString(self):
        return self.string

    def __repr__(self):
        return f"{self.__class__.__name__}: '{self.string}'"

    def __str__(self):
        return f"{self.__class__.__name__}: '{self.string}'"

class ItalicsText(Text):
    pass
    # def __str__(self):
    #     return f"ItalicsText: {self.string}"

class ManaText(Text):
    def __init__(self, string):
        super().__init__(string)
        self.mana_string = string[1:-1].replace("/", "")

    def getManaList(mana_list):
        return [ManaText(m) for m in re.findall("({.+?})", mana_list)]

# if __name__ == "__main__":
#     r = "Hexproof\nDevoid <i>(This creature has no color.)</i>\n{3}, {T}: <i>Add {U}{R} to</i> your mana pool."
#     rules = Rules(r)

