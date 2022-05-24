geany_theme_to_spyder = {}
geany_theme_to_spyder["default"] = "Normal text"
geany_theme_to_spyder["comment"] = "Comment"
geany_theme_to_spyder["string"] = "String"
geany_theme_to_spyder["number"] = "Number"
geany_theme_to_spyder["keyword"] = "Keyword"
geany_theme_to_spyder["default[1]"] = "Background"  # 1 is the second value such as in `default=#b8d1d8;#000;false;false`
# geany_theme_to_spyder[""] = "Builtin"
# ^ identifier=default  # in epsilon-dark (#b8d1d8)
geany_theme_to_spyder["type"] = "Definition"
# ^ class=type  # in epsilon-dark (#2f9494)
# #ffffff

# Next, account for structural differences:
# Geany:
# - `class`, `def`, and `print` are the same
# - `self` is default (no highlighting)
# Spyder:
# - `class` and `def` are Keyword
# - `object` and `print` are Builtin
#   - since separate in Spyder, maybe use same color&bold as Keyword but italic
# - `self` is Instance
#   - since separate in Spyder, maybe use same color&bold as normal but italic
geany_theme_to_spyder_copy_italic = {}
geany_theme_to_spyder_copy_italic["Builtin"] = "Keyword"
geany_theme_to_spyder_copy_italic["Instance"] = "Normal text"

# Not yet known:
# Geany:
# - `label=default,bold`

# Known to not be in Spyder:
# Geany:
# - function=default
# - parameter=default



