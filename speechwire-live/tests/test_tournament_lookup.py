import unittest

from speechwire_live.client.tournament_lookup import Tournament, parse_todays_tournaments

TODAY = "Nov. 7, 2026"


def row(date, name, tournid, location, linked=True):
    name_cell = (
        f'<td class="bluetablesmall"><a href="p-tournament.php?tournid={tournid}">{name}</a></td>'
        if tournid
        else f'<td class="bluetablesmall">{name}</td>'
    )
    more = "<td>More info</td>" if linked else "<td></td>"
    return f"<tr><td>{date}</td>{name_cell}{more}<td>HS</td><td>In person</td><td>{location}</td></tr>"


def calendar(*rows):
    title = "<tr>" + "<td>TOURNAMENT NAME</td>" * 6 + "</tr>"
    header = "<tr>" + "".join(
        f"<td>{h}</td>" for h in ["Date", "Tournament Name", "More info", "Level", "Platform", "Location"]
    ) + "</tr>"
    return f'<html><body><table class="bluetable">{title}{header}{"".join(rows)}</table></body></html>'


class ParseTodaysTournamentsTests(unittest.TestCase):
    def test_returns_only_todays_linked_tournaments_with_their_ids(self):
        html = calendar(
            row(TODAY, "Alpha Invitational", "111", "Omaha, NE"),
            row("Nov. 8, 2026", "Tomorrow Classic", "222", "Lincoln, NE"),
            row(TODAY, "Beta Open", "333", "Kearney, NE"),
            row(TODAY, "No Page Yet", None, "Elsewhere", linked=False),
        )
        self.assertEqual(
            parse_todays_tournaments(html, TODAY),
            [
                Tournament("Alpha Invitational", "111", "Omaha, NE"),
                Tournament("Beta Open", "333", "Kearney, NE"),
            ],
        )

    def test_no_tournaments_today_returns_an_empty_list(self):
        html = calendar(row("Nov. 8, 2026", "Tomorrow Classic", "222", "Lincoln, NE"))
        self.assertEqual(parse_todays_tournaments(html, TODAY), [])


if __name__ == "__main__":
    unittest.main()
