from shiny import App, Inputs, Outputs, Session, render, ui, reactive
from faicons import icon_svg
from shinywidgets import output_widget, render_widget
import pandas as pd
from pathlib import Path

from utils.processor import get_summary_data
from utils.plotter import get_map, plot_top_ten, plot_gauge_chart, plot_accessibility
from utils.helper_text import about_text, disclaimer_text, info_modal, github_text

DATA = pd.read_csv(
    Path().resolve() / "data" / "ncr_data_cleaned.csv",
)

SUMMARY_DATA = get_summary_data(df=DATA)

app_ui = ui.page_navbar(
    ui.nav_panel(
        "Overview",
        ui.layout_column_wrap(
            ui.value_box(
                "Total chargepoints",
                SUMMARY_DATA.total_chargers,
                showcase=icon_svg("plug"),
            ),
            ui.card(output_widget("_inservice")),
            ui.value_box(
                "County with the most chargepoints",
                SUMMARY_DATA.county_with_most_chargers,
                showcase=icon_svg("flag"),
            ),
            ui.card(output_widget("_payment_req")),
            ui.card(output_widget("_all_day_access")),
            fill=False,
            height="250px",
        ),
        ui.card(
            ui.card_header(
                """
                Bar charts of the top ten counties,
                location types, device manufacturers,
                owners, and controllers with the highest number of 
                chargepoints in the UK. Hover on each 
                bar to see the exact number of charge 
                devices.
                """
            ),
            output_widget("_top_ten"),
        ),
    ),
    ui.nav_panel(
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
                        ui.card_header(
                            """
                        The following plots show the percentage of chargepoints
                        based on 24-hour accessibility, payment and subscription
                        requirements. Hover on the charts to see the actual 
                        number of chargepoints in each segment of the donut charts.
                        """
                        ),
                        output_widget("_accessibility"),
                        height="360px",
                    ),
                ),
            ),
            ui.card(
                ui.card_header(
                    """
                Map of EV chargepoints in the UK as obtained from the
                National Chargepoint Registry UK (NCR). Hover on the 
                icon to see more information about each chargepoint. You
                can activate the fullscreen mode by clicking on the disjointed
                square icon.
                """
                ),
                ui.output_ui("_map"),
            ),
        ),
    ),
    sidebar=ui.sidebar(
        ui.card(about_text()),
        ui.card(disclaimer_text()),
        ui.card(github_text()),
        width=400,
    ),
    title="UK EV CHARGEPOINTS",
    fillable=True,
)


def server(input: Inputs, output: Outputs, session: Session):

    info_modal()

    @render_widget
    def _top_ten():
        return plot_top_ten(top_ten=SUMMARY_DATA.top_ten)

    @render_widget
    def _inservice():
        return plot_gauge_chart(
            value=SUMMARY_DATA.in_service_chargers,
            title="In service",
        )

    @render_widget
    def _payment_req():
        return plot_gauge_chart(
            value=SUMMARY_DATA.non_payment_chargers,
            title="Payment not required",
        )

    @render_widget
    def _all_day_access():
        return plot_gauge_chart(
            value=SUMMARY_DATA.all_day_chargers,
            title="Accessible all day",
        )

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
