from fasthtml.common import *
from monsterui.all import *
from dotenv import load_dotenv
import requests, csv, io

# Load environment variables from .env file
load_dotenv()


def get_sheet_data(sheet_url):
    response = requests.get(sheet_url)
    if response.status_code != 200:
        return {}
    data = response.text
    reader = csv.DictReader(io.StringIO(data))
    json_list = list(reader)
    return json_list


app, rt = fast_app(hdrs=Theme.blue.headers(), live=True)


def ScholarshipRow(icon, name, desc, is_link):
    if is_link:
        return Li(cls="-mx-1")(
            A(
                DivLAligned(
                    UkIcon(icon), Div(P(name), P(desc, cls=TextPresets.muted_sm))
                ),
                href=desc,
                target="_blank",
            )
        )
    return Li(cls="-mx-1")(
        A(DivLAligned(UkIcon(icon), Div(P(name), P(desc, cls=TextPresets.muted_sm))))
    )


def Scholarship(s):
    details = (
        ("mail", "Öppnar", s.get("application-open", ""), False),
        ("bell", "Deadline", s.get("application-close", ""), False),
        ("link", "Ansökan", s.get("application-link", ""), True),
    )

    return Card(
        NavContainer(*[ScholarshipRow(*row) for row in details], cls=NavT.secondary),
        header=(
            H3(s.get("scholarship-name", "")),
            Subtitle(s.get("scholarship-summary", "")),
        ),
        body_cls="pt-0",
    )


@rt("/")
def get():
    scholarships = get_sheet_data(os.getenv("SCHOLARSHIPS_URL"))

    return Titled(
        "Välkommen till stipendielistan! 🇸🇪🇺🇸",
        P(
            "Här samlar vi svenska och amerikanska stipendier för kandidatstudier i USA.",
            cls=TextPresets.muted_sm,
        ),
        *[Scholarship(s) for s in scholarships],
    )


serve()
