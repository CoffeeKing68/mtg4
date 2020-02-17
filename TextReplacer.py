from re import compile, sub, split
from pprint import pprint


class Rep:
    def __init__(self, search, replace):
        self.search = search
        self.replace = replace

    def substitute(self, text):
        if text:
            return sub(self.search, self.replace, text)
        else:
            return None


class Text:
    def __init__(self, text):
        self.text = text


class ItalicsText(Text):
    pass


class RegularText(Text):
    pass


class ManaText(Text):
    pass


class TextMapper():
    def __init__(self):
        self.formattedText = None

    @staticmethod
    def flavorReplacements():
        return {
            "flavor_dash": Rep(r"(?<!\n)(\u2014.+)$", r"\n\1"),
        }

    @staticmethod
    def rulesReplacements():
        return {
            "flavor_dash": Rep(r"(?<!\n)(\u2014.+)$", r"\n\1"),
            #
            "prowess": Rep(r"(Prowess.*)(?<!<i>)(\(Whenever you cast a noncreature spell, this creature gets \+1/\+1 until end of turn.\))(?<!</i>)", r"\1<i>\2</i>"),
            "suspend": Rep(r"(Suspend.*)(?<!<i>)(\(Rather than cast this card from your hand, you may pay .+ and exile it with a time counter on it. At the beginning of your upkeep, remove a time counter. When the last is removed, cast it without paying its mana cost.\))(?<!</i>)", r"\1<i>\2</i>"),
            "land_taps": Rep(r"(?<!<i>)(\({T}: Add {.*}\.\))(?<!</i>)", r"<i>\1</i>"),
            "landfall": Rep(r"(?<!<i>)(Landfall [-|\u2014] )(?<!</i>)(?=If you had a land enter the battlefield under your control this)", "<i>Landfall \u2014 </i>"),
            "spectacle": Rep(r"(Spectacle.*)(?<!<i>)(\(You may cast this spell for its spectacle cost rather than its mana cost if an opponent lost life this turn.\))(?<!</i>)", r"\1<i>\2</i>"),
            "escalate": Rep(r"(Escalate\u2014.*)(?<!<i>)(\(Pay this cost for each mode chosen beyond the first.\))(?<!</i>)", r"\1<i>\2</i>"),
            "revolt": Rep(r"(?<!<i>)(Revolt)(?<!</i>)(.*permanent you controlled left the battlefield this turn\..*)", r"<i>\1</i>\2"),
            "levels": Rep(r"(Level up.*)(?<!<i>)(\(\{.*\}: Put a level counter on this. Level up only as a sorcery\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "trample_help": Rep(r"([T|t]rample.*)(?<!<i>)(\(It can deal excess combat damage to the player or planeswalker it's attacking\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "delve": Rep(r"([D|d]elve.*)(?<!<i>)(\(Each card you exile from your graveyard while casting this spell pays for \{1\}\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "clue_help": Rep(r"([I|i]nvestigate.*)(?<!<i>)(\(.*colorless Clue artifact token .*with \"\{2\}, Sacrifice this artifact: Draw a card.\"\))(?<!</i>)", r"\1<i>\2</i>"),
            "undergrowth": Rep(r"(?<!<i>)(Undergrowth [-|\u2014] )(?<!</i>)(?=.*creature cards+ in your graveyard.*)", "<i>Undergrowth \u2014 </i>"),
            "scry_help": Rep(r"([S|s]cry \d+.*)(?<!<i>)(\(Look at .* You may .* of your library.*\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "flashback": Rep(r"([F|f]lashback.*)(?<!<i>)(\(You may cast that card from your graveyard for its flashback cost\. Then exile it\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "cycle": Rep(r"([C|c]ycl[e|ing].*)(?<!<i>)(\(.*[D|d]iscard this card: Draw a card\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "ferocius": Rep(r"(?<!<i>)(Ferocious [-|\u2014] )(?<!</i>)(?=.*If you control a creature with power 4 or greater.*)", "<i>Ferocious \u2014 </i>"),
            "cascade": Rep(r"([C|c]ascade.*)(?<!<i>)(\(When you cast this spell, exile cards from the top .* in a random order\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "monstrous": Rep(r"(Monstrosity .*)(?<!<i>)(\(If this creature isn't monstrous.*and it becomes monstrous\.\))(?<!</i>)", r"\1<i>\2</i>"),
            # "planeswalker": PlaneswalkerRep(),
            "phyrexian_mana": Rep(r"(?<!<i>)(\(\{.+\} can be paid with either.+life\.\))(?<!</i>)", r"<i>\1</i>"),
            "retrace": Rep(r"([R|r]etrace.*)(?<!<i>)(\(You may cast instant and sorcery cards from your graveyard by discarding a land card in addition to paying their other costs\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "devoid": Rep(r"([D|d]evoid.*)(?<!<i>)(\(This card has no color.\))(?<!</i>)", r"\1<i>\2</i>"),
            "colorless_mana": Rep(r"(?<!<i>)(\(\{C\} represents colorless mana.\))(?<!</i>)", r"<i>\1</i>"),
            "landwalk": Rep(r"(walk.*)(?<!<i>)(\(\D+ be blocked as long as defending player controls a\D+\.\))(?<!</i>)",
                            r"\1<i>\2</i>"),
            "colorless_cards": Rep(r"(?<!<i>)(\((Cards with no colored mana in their mana costs are colorless\D*\.)\))(?<!</i>)",
                                   r"<i>\1</i>"),
            "exalted": Rep(r"([E|e]xalted.*)(?<!<i>)(\(Whenever a creature you control attacks alone, that creature gets \+1/\+1 until end of turn\.\))(?<!</i>)",
                           r"\1<i>\2</i>"),

            "flash": Rep(r"([F|f]lash.*)(?<!<i>)(\(You may cast this spell any time you could cast an instant\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "surveil": Rep(r"([S|s]urveil.*)(?<!<i>)(\(To surveil .+ in any order\.\))(?<!</i>)", r"\1<i>\2</i>"),
        }

    def map(self, text, flavor=False):
        if text:
            if flavor:
                for rep in self.flavorReplacements().values():
                    text = rep.subsitute(text)
            else:
                for rep in self.rulesReplacements().values():
                    text = rep.substitute(text)
                self.formattedText = text
        else:
            self.formattedText = ""
        return self

    def prepareForRender(self):
        newText = {}
        for i, paragraph in enumerate(self.formattedText.split("\n")):
            italicsContext = False
            newText[i] = []

            for multiWords in split(r"/(<i>.+<\/i>)/g", paragraph):
                italicsContext = multiWords.startswith('<i>')

                for word in [w for w in split(r"/({.+?})/g", multiWords) if w]:
                    if (word.startswith('{')):
                        newText[i].append(ManaText(word))
                    elif italicsContext:
                        newText[i].append(ItalicsText(
                            sub(r"/[<i>|<\/i>]/g", "", word)))
                    else:
                        newText[i].append(RegularText(word))
        return newText


if __name__ == "__main__":
    s = "Flash (You may cast this spell any time you could cast an instant.)\nWhenever you cast a spell during an opponent's turn, put a +1/+1 counter on Brineborn Cutthroat."
    surveil = "Flash\nFlying\nWhen Dream Eater enters the battlefield, surveil 4. When you do, you may return target nonland permanent an opponent controls to its owner's hand. (To surveil 4, look at the top four cards of your library, then put any number of them into your graveyard and the rest on top of your library in any order.)"
    castle = "Castle Vantress enters the battlefield tapped unless you control an Island.\n{T}: Add {U}.\n{2}{U}{U}, {T}: Scry 2."
    replacer = TextMapper()
    pprint(replacer.map(castle).formattedText)