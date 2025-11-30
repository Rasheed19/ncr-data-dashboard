import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from faicons import icon_svg
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_widget

from utils.helper_text import (
    about_text,
    access_text,
    disclaimer_text,
    github_text,
    info_modal,
    map_text,
    top_ten_text,
)
from utils.plotter import get_map, plot_accessibility, plot_top_ten
from utils.processor import get_summary_data

load_dotenv()

DATA = pd.read_csv(
    Path().resolve() / "data" / "ncr_data_cleaned.csv",
)

SUMMARY_DATA = get_summary_data(df=DATA)

page_dependencies = ui.head_content(
    ui.HTML(
        f"""
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id={os.getenv("GA_ID")}"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{os.getenv("GA_ID")}');
        </script>
        """
    ),
    ui.include_css("./www/style.css"),
)

overview_ui = ui.nav_panel(
    "Overview",
    ui.layout_column_wrap(
        *[
            ui.value_box(
                title,
                value,
                *tagchild,
                showcase=icon_svg(icon),
            )
            for title, value, tagchild, icon in zip(
                [
                    "Total chargepoints",
                    "In service",
                    "County with the most chargepoints",
                    "Payment not required",
                    "Accessible all day",
                ],
                [
                    f"{SUMMARY_DATA.total_chargers:,}",
                    f"{SUMMARY_DATA.in_service_chargers:,}",
                    SUMMARY_DATA.county_with_most_chargers,
                    f"{SUMMARY_DATA.non_payment_chargers:,}",
                    f"{SUMMARY_DATA.all_day_chargers:,}",
                ],
                [
                    "",
                    f"{(SUMMARY_DATA.in_service_chargers * 100 / SUMMARY_DATA.total_chargers):.2f}% of total chargepoints",
                    "",
                    f"{(SUMMARY_DATA.non_payment_chargers * 100 / SUMMARY_DATA.total_chargers):.2f}% of total chargepoints",
                    f"{(SUMMARY_DATA.all_day_chargers * 100 / SUMMARY_DATA.total_chargers):.2f}% of total chargepoints",
                ],
                [
                    "plug",
                    "plug-circle-check",
                    "flag",
                    "money-check-dollar",
                    "calendar-check",
                ],
            )
        ],
        fill=False,
        height="250px",
    ),
    ui.card(
        top_ten_text(),
        output_widget("_top_ten"),
    ),
)

county_ui = ui.nav_panel(
    "UK county chargepoint information",
    ui.tags.div(
        ui.row(
            ui.column(
                2,
                ui.input_selectize(
                    "county",
                    "Enter or select a UK county",
                    choices=SUMMARY_DATA.counties,
                    selected="Edinburgh",
                    multiple=False,
                    options=(
                        {
                            "placeholder": "Enter or select a county",
                            "create": True,
                        }
                    ),
                ),
                ui.value_box(
                    "Number of chargers",
                    ui.output_text("_county_charger_count"),
                    showcase=icon_svg("plug"),
                ),
            ),
            ui.column(
                10,
                ui.card(
                    access_text(),
                    output_widget("_accessibility"),
                    height="360px",
                ),
            ),
        ),
        ui.card(
            map_text(),
            ui.output_ui("_map"),
        ),
    ),
)

sidebar = ui.sidebar(
    ui.card(about_text()),
    ui.card(disclaimer_text()),
    ui.card(github_text()),
    width=400,
)

app_ui = ui.page_navbar(
    page_dependencies,
    overview_ui,
    county_ui,
    sidebar=sidebar,
    title="UK EV CHARGEPOINTS",
    fillable=True,
)


def server(input: Inputs, output: Outputs, session: Session):
    info_modal()

    @render_widget
    def _top_ten():
        return plot_top_ten(top_ten=SUMMARY_DATA.top_ten)

    @reactive.calc
    @reactive.event(input.county)
    def _get_filtered_data() -> tuple[str, pd.DataFrame]:
        county = "Edinburgh" if input.county() == "" else input.county()
        return county, DATA[DATA["County"] == county]

    @render.ui
    def _map():
        return get_map(_get_filtered_data()[1])

    @render.text
    def _county_charger_count():
        _, filtered_data = _get_filtered_data()
        return f"{filtered_data.shape[0]}"

    @render_widget
    def _accessibility():
        return plot_accessibility(df=_get_filtered_data()[1])


app = App(app_ui, server)
