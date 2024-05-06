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
            The information contained in this dashboard **should be taken as an indication
            to the distribution of the chargepoints in the UK and not the exact 
            figures**. **It is meant for educational purpose only and not to be used to make
            decisions**. It is believed that some chargepoints might not be logged to
            the National Chargepoint Registry at the time of visiting this dashboard.

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
            The source code for this dashboard can be foud in 
            this [link](https://github.com/Rasheed19/ncr-data-dashboard). 
            Information about how to run the dashboard locally and how
            to deploy it to various platforms can also be found in the 
            link.       
            """
        ),
    )


def info_modal():
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
        )
    )
