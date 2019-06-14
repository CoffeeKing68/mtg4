import re

class Bounds():
    standard_bound_names = ["start", "end", "center", "full"]
    """
    :param kwargs: {start: 0, full: 20}.
    start=None, center=None, end=None, full=None
    """
    def __init__(self, **kwargs):
        self.__bounds = {key: val for key, val in kwargs.items() if Bounds.is_valid_bound_key(key)}
        self.__eval_bounds = {}

        if len(self.__bounds) == 2:
            self.determine_bounds()
        else:
            raise InsufficientBoundsError("Not enough bounding descriptors.")

    def __bound_property_maker(bound_name):
        def getter(self):
            return self.__eval_bounds.get(bound_name)
        def setter(self, value):
            self.__eval_bounds[bound_name] = value
        def deleter(bound_name):
            del self.__eval_bounds[bound_name]
        return property(getter, setter, deleter)

    start = __bound_property_maker("start")
    end = __bound_property_maker("end")
    center = __bound_property_maker("center")
    full = __bound_property_maker("full")

    def determine_bounds(self):
        # first "plot" points we have on quantifiable line
        plot = {}
        available_bounds = self.__bounds
        if "start" in self.__bounds:
            plot[0] = available_bounds.pop("start")
        if "center" in self.__bounds:
            plot[50] = available_bounds.pop("center")
        if "end" in self.__bounds:
            plot[100] = available_bounds.pop("end")

        if len(plot) < 2: # Don't look for percent defs if we have all defs already
            for bound in list(available_bounds):
                pct = Bounds.parse_pct_key(bound)
                if pct is not None:
                    plot[int(pct)] = available_bounds.pop(bound)

        if "full" in self.__bounds and len(plot) == 1: # if full was passed in
            pct, value = list(plot.items())[0]
            self.full = self.__bounds["full"]
        elif len(plot) == 2: # found 2 bound defs
            (pct, value), (bpct, bval) = sorted(plot.items())
            self.full = (bval - value) / (bpct - pct) * 100
        else:
            raise InsufficientBoundsError("Not enough bounds.")

        self.end = (1 - pct / 100) * self.full + value
        self.start = value - pct * self.full / 100
        self.center = self.start + self.full / 2

    def is_valid_bound_key(key):
        """
        Checks if key is a recognised bound name or percentage
        :param key: Potentially valid bound (either in standard_bound_names or is in form p<pct>)
        """
        return key in Bounds.standard_bound_names or Bounds.parse_pct_key(key) is not None

    def is_valid_pct_bound_key(pct_key):
        if pct_key[0].upper() == "P": # P or p
            try:
                Bounds.parse_pct_key(pct_key)
                return True
            except ValueError:
                pass
        return False

    def parse_pct_key(pct_key):
        try:
            return float(pct_key[1:])
        except:
            return None

    @property
    def bounds(self):
        return self.__eval_bounds

    def __getitem__(self, key):
        if key in self.__eval_bounds:
            return self.__eval_bounds[key]
        else:
            return self.get_percent(key)

    def get_percent(self, key):
        if isinstance(key, (int, float)): # is this a number?
            pct = key
        elif isinstance(key, str):
            if key[0].upper() == "P":
                key = key[1:]
            pct = float(key)
        else:
            raise ValueError("Pass in an int, float, <percent_string> or P/p<percent_string>")
        return self.start + pct + self.full / 100

    def __repr__(self):
        return f"Bounds: {self.__eval_bounds}"

    def shift(self, value):
        self.start += value
        self.center += value
        self.end += value

class InsufficientBoundsError(Exception):
    """Raised when Bounds object does not have enough bounding descriptors."""
    pass

if __name__ == "__main__":
    bounds = Bounds(P50=80, full=120)
    print(bounds)
    print(bounds[50])
    print(bounds[50.0])
    print(bounds["P50"])
    print(bounds["p50"])
