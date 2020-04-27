from collections import defaultdict

from app import utils


def get_single_line_chart_hist(json, is_new_stats):
    stats = defaultdict(lambda: defaultdict(list))
    for stats_type in json:
        last_value = 0
        for date in json[stats_type]:
            date_obj = utils.parse_date(date)
            date_str = utils.format_date(date_obj)

            stats[stats_type]["labels"].append(date_str)
            stats[stats_type]["total"] = json[stats_type][date]
            curr_value = json[stats_type][date]

            if is_new_stats:
                new_value = curr_value - last_value
                last_value = curr_value
            else:
                new_value = curr_value

            stats[stats_type]["data"].append(new_value)

    return stats
