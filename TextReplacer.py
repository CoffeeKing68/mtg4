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
        self.formattedText = ""

    @staticmethod
    def flavorReplacements():
        return {
            # "flavor_dash": Rep(r"(?<!\n)(?<=\")(\u2014.+)$", r"\n\1"),
            "flavor_dash": Rep(r"(.*\")(\s*)(\u2014)(\s*)(.+)$", r"\1\n\3\5"),
        }

    @staticmethod
    def rulesReplacements():
        return {
            # "flavor_dash": Rep(r"(?<!\n)(?<!<i>)(\u2014.+)$", r"\n\1"),
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
            "flashback": Rep(r"([F|f]lashback.*)(?<!<i>)(\(You may cast .+ flashback cost\. Then exile it\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "cycle": Rep(r"([C|c]ycl[e|ing].*)(?<!<i>)(\(.*[D|d]iscard this card: Draw a card\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "ferocius": Rep(r"(?<!<i>)(Ferocious [-|\u2014] )(?<!</i>)(?=.*If you control a creature with power 4 or greater.*)", "<i>Ferocious \u2014 </i>"),
            "cascade": Rep(r"([C|c]ascade.*)(?<!<i>)(\(When you cast this spell, exile cards from the top .* in a random order\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "monstrous": Rep(r"(Monstrosity .*)(?<!<i>)(\(If this creature isn't monstrous.*and it becomes monstrous\.\))(?<!</i>)", r"\1<i>\2</i>"),
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
            "planeswalker": Rep(r"(\u2212)(.+)", r"-\2"),
            "escape": Rep(r"([E|e]scape)(\n)(\u2014)({.+?},.*)(?<!<i>)(\(You may cast this card from your graveyard for its escape cost.\))(?<!</i>)", r"\1\3\4<i>\5</i>"),
            "adventure": Rep(r"(?<!<i>)(\(Then exile this card. You may cast the creature later from exile\.\))(?<!</i>)", r"<i>\1</i>"),
            "afterlife": Rep(r"([A|a]fterlife.*)(?<!<i>)(\(When this creature dies.+white and black Spirit creature token with flying\.\))(?<!</i>)",
                             r"\1<i>\2</i>"),
            "saga_info": Rep(r"(?<!<i>)(\(As this Saga enters and after your draw step, add a lore counter\. Sacrifice after III\.\))(?<!</i>)", r"<i>\1</i>"),
            "saga_newline": Rep(r"(I{1,3}) (\n)*—", r"\1 —"),
            "meld": Rep(r"(?<!<i>)(\(Melds with .+\.\))(?<!</i>)", r"<i>\1</i>"),
            "partner_with": Rep(r"(Partner with .+ )(?<!<i>)(\(When this .+\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "hideaway": Rep(r"(?<=Hideaway )(?<!<i>)(\(This land enters the battlefield tapped. When .+ library\.\))(?<!</i>)", r"<i>\1</i>"),
            "proliferate": Rep(r"([P|p]roliferate.*)(?<!<i>)(\(Choose any number of permanents .+\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "strive": Rep(r"(?<!<i>)([S|s]trive \u2014 )(?<!</i>)(This spell .+\.)", r"<i>\1</i>\2"),
            "first_strike": Rep(r"(First strike )(?<!<i>)(\(This creature deals .+ first strike\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "converge": Rep(r"(?<!<i>)(Converge)(?<!</i>)( \u2014 .+ where X is the number of colors of mana spent .+)", r"<i>\1</i>\2"),
            "morph": Rep(r"([M|m]orph .+)(?<!</i>)(\(You may cast this card .+\. Turn it face up any time for its morph cost\.\))(?<!</i>)", r"\1<i>\2</i>"),
            "fuse": Rep(r"([F|f]use .*)(?<!</i>)(\(You may cast one or both halves of this card from your hand.\))(?<!</i>)", r"\1<i>\2</i>"),
            "aftermath": Rep(r"([A|a]ftermath .*)(?<!</i>)(\(Cast this spell only from your graveyard. Then exile it.\))(?<!</i>)", r"\1<i>\2</i>"),

            # "remove_partner_with": Rep(r"(Partner with .+)( <i>\(When this .+\.\)</i>)", r"\1"),
            "remove_partner_with": Rep(r"(Partner with .+)( <i>\(When this .+\.\)</i>)", r"\1"),
        }

    def map(self, text, flavor=False):
        if text:
            if flavor:
                for rep in self.flavorReplacements().values():
                    text = rep.substitute(text)
            else:
                for rep in self.rulesReplacements().values():
                    # print(len(text.splitlines()))
                    text = rep.substitute(text)
            self.formattedText = text
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


def test_replacement(mechanic, index, flavor=False):
    if flavor:
        tests = flavor_tests
    else:
        tests = rules_tests
    replacer = TextMapper()
    print(repr(replacer.map(tests[mechanic][index][0], flavor).formattedText))

    equals = []
    for i, (before, after) in enumerate(tests[mechanic]):
        print(i)
        print(repr(before))
        print(repr(after))
        formatted_text = replacer.map(before, flavor).formattedText
        print(repr(formatted_text))
        eq = formatted_text == after
        print(eq)
        equals.append(eq)
    print(all(equals))


if __name__ == "__main__":
    flavor_tests = {
        "flavor_dash": [
            [
                "\"Only the weak imprison themselves behind walls. We live free under the wind, and our freedom makes us strong.\" \u2014Zurgo, khan of the Mardu",
                '"Only the weak imprison themselves behind walls. We live free under the wind, and our freedom makes us strong."\n\u2014Zurgo, khan of the Mardu'
            ],
            [
                '\"Not Robert the Second. Aerys the Third!\" \u2014 Tyrion',
                '\"Not Robert the Second. Aerys the Third!\"\n\u2014Tyrion',
            ],
            [
                '\"Cersei liked to think of herself as Lord Tywin with teats, but she was wrong.\" \u2014Jaime Lannister',
                '\"Cersei liked to think of herself as Lord Tywin with teats, but she was wrong.\"\n\u2014Jaime Lannister',
            ],
            [
                '<i>"No other knight in the realm inspires such terror in our enemies."\u2014Tywin Lannister</i>',
                '<i>"No other knight in the realm inspires such terror in our enemies."\n\u2014Tywin Lannister</i>',
            ]
        ]
    }

    rules_tests = {
        "first_strike": [
            [
                "First strike (This creature deals combat damage before creatures without first strike.)\nWhenever Odric, Master Tactician and at least three other creatures attack, you choose which creatures block this combat and how those creatures block.",
                "First strike <i>(This creature deals combat damage before creatures without first strike.)</i>\nWhenever Odric, Master Tactician and at least three other creatures attack, you choose which creatures block this combat and how those creatures block."
            ]
        ],
        "converge": [
            [
                "Converge \u2014 You draw X cards and you lose X life, where X is the number of colors of mana spent to cast Painful Truths.",
                "<i>Converge</i> \u2014 You draw X cards and you lose X life, where X is the number of colors of mana spent to cast Painful Truths."
            ]
        ],
        "remove_partner_with": [
            [
                "Partner with Trynn, Champion of Freedom (When this creature enters the battlefield, target player may put Trynn into their hand from their library, then shuffle.)\nMenace\nSacrifice a Human: Put a +1/+1 counter on Silvar, Devourer of the Free. It gains indestructible until end of turn.",
                "Partner with Trynn, Champion of Freedom\nMenace\nSacrifice a Human: Put a +1/+1 counter on Silvar, Devourer of the Free. It gains indestructible until end of turn.",
            ],
            [
                'Partner with Silvar, Devourer of the Free (When this creature enters the battlefield, target player may put Silvar into their hand from their library, then shuffle.)\nAt the beginning of your end step, if you attacked this turn, create a 1/1 white Human Soldier creature token.',
                'Partner with Silvar, Devourer of the Free\nAt the beginning of your end step, if you attacked this turn, create a 1/1 white Human Soldier creature token.',
            ]
        ],
        "morph": [
            [
                "Morph {B} (You may cast this card face down as a 2/2 creature for {3}. Turn it face up any time for its morph cost.)\nWhenever another nontoken creature you control dies, draw a card.",
                "Morph {B} <i>(You may cast this card face down as a 2/2 creature for {3}. Turn it face up any time for its morph cost.)</i>\nWhenever another nontoken creature you control dies, draw a card.",
            ]
        ],
        "flashback": [
            [
                "Create five 1/1 white Human creature tokens. If this spell was cast from a graveyard, create ten of those tokens instead.\nFlashback {7}{W}{W} (You may cast this card from your graveyard for its flashback cost. Then exile it.)",
                "Create five 1/1 white Human creature tokens. If this spell was cast from a graveyard, create ten of those tokens instead.\nFlashback {7}{W}{W} <i>(You may cast this card from your graveyard for its flashback cost. Then exile it.)</i>",
            ]
        ],
        "fuse": [
            [
                "Destroy target artifact.\nFuse (You may cast one or both halves of this card from your hand.)",
                "Destroy target artifact.\nFuse <i>(You may cast one or both halves of this card from your hand.)</i>",
            ]
        ],
        "aftermath":[
            [
                "Aftermath (Cast this spell only from your graveyard. Then exile it.)\nTap up to two target creatures your opponents control. Creatures you control gain vigilance until end of turn.",
                "Aftermath <i>(Cast this spell only from your graveyard. Then exile it.)</i>\nTap up to two target creatures your opponents control. Creatures you control gain vigilance until end of turn.",
            ]
        ]
    }

    test_replacement("aftermath", 0, False)
    # text = "\"Only the weak imprison themselves behind walls. We live free under the wind, and our freedom makes us strong.\" \u2014Zurgo, khan of the Mardu"
