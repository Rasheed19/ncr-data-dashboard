from shiny import ui


def about_text() -> ui.Tag:
    return ui.tags.div(
        ui.h4("About"),
        ui.markdown(
            """
            This dashboard showcases the distribution of chargepoints
            in the UK. It uses the data downloaded from the National
            Chargepoint Registry UK (NCR) which can be found in this
            [link](https://www.gov.uk/guidance/find-and-use-data-on-public-electric-vehicle-chargepoints).
            """
        ),
    )


def disclaimer_text() -> ui.Tag:
    return ui.tags.div(
        ui.h4("Disclaimer"),
        ui.markdown(
            """
            The information contained in this dashboard **_should be taken as an indication
            to the distribution of the chargepoints in the UK and not the exact
            figures. It is meant for educational purpose only and not to be used to make
            decisions_**.

            **_The National Chargepoint Registry will be decommissioned on 28th November 2024.
            Thus, the data behind this dashboard will no longer be updated from that date.
            Read more about these changes [here](https://www.cenex.co.uk/news/uuks-national-chargepoint-registry-managed-by-cenex-to-be-closed-down/)_**.

            The dataset from the NCR have been cleaned to remove chargepoints
            without a unique identification number, those with missing counties and
            incorrect latitude and longitude coordinates.
            """
        ),
    )


def github_text() -> ui.Tag:
    return ui.tags.div(
        ui.h4("Cloan this dashboard"),
        ui.markdown(
            """
            The source code for this dashboard can be found in
            this [link](https://github.com/Rasheed19/ncr-data-dashboard).
            Information about how to run the dashboard locally and how
            to deploy it to various platforms can also be found in the
            link.
            """
        ),
    )


def info_modal() -> None:
    ui.modal_show(
        ui.modal(
            ui.strong(ui.h3("UK CHARGEPOINTS DASHBOARD")),
            ui.p(
                """Exploring the Distribution of Chargepoints
                in the UK National Chargepoint Registry (NCR)
                """
            ),
            ui.hr(),
            about_text(),
            ui.hr(),
            disclaimer_text(),
            size="l",
            easy_close=True,
            footer=ui.modal_button(
                "Close",
                class_="btn btn-primary",
            ),
            style="""
             .modal-dialog {
                margin-top: 20px !important;  /* Adjust this value as needed */
                overflow-y: hidden !important;
            }
            """,
        )
    )


def map_text() -> ui.Tag:
    return ui.card_header(
        """
        Map of EV chargepoints in the UK as obtained from the
        National Chargepoint Registry UK (NCR). Hover on the
        icon to see more information about each chargepoint. You
        can activate the fullscreen mode by clicking on the disjointed
        square icon.
        """
    )


def access_text() -> ui.Tag:
    return ui.card_header(
        """
        The following plots show the percentage of chargepoints
        based on 24-hour accessibility, payment and subscription
        requirements. Hover on the charts to see the actual
        number of chargepoints in each segment of the donut charts.
        """
    )


def top_ten_text() -> ui.Tag:
    return ui.card_header(
        """
        Bar charts of the top ten counties,
        location types, device manufacturers,
        owners, and controllers with the highest number of
        chargepoints in the UK. Hover on each
        bar to see the exact number of charge
        devices.
        """
    )
