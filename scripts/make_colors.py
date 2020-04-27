import json
import requests
import seaborn as sns

from collections import defaultdict


def main():
    r = requests.get("https://corona.lmao.ninja/v2/historical?lastdays=1")
    data = r.json()

    countries = defaultdict(list)
    for country in data:
        countries[country["country"]].append(country["province"])

    countries_dict, states_dict = get_color_dicts(countries)

    r = requests.get("https://corona.lmao.ninja/v2/jhucsse/counties")
    data = r.json()

    us_states = defaultdict(list)
    for state in data:
        us_states[state["province"]].append(state["county"])

    us_states_dict, counties_dict = get_color_dicts(us_states)
    states_dict.update(us_states_dict)

    with open("colors.json", "w") as f:
        json.dump(
            {
                "countries": countries_dict,
                "states": states_dict,
                "counties": counties_dict,
            },
            f,
        )


def get_color_dicts(data):
    outer_dict = {}
    inner_dict = {}
    outer_colors = sns.color_palette("hls", len(data)).as_hex()

    for i, outer_data in enumerate(data):
        outer_dict[outer_data] = outer_colors[i]
        inner_list = [x for x in data[outer_data] if x is not None]

        if inner_list:
            inner_colors = sns.color_palette("hls", len(inner_list)).as_hex()
            for j, innder_data in enumerate(inner_list):
                inner_dict[innder_data] = inner_colors[j]

    return outer_dict, inner_dict


if __name__ == "__main__":
    main()
