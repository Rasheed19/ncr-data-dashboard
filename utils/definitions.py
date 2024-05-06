class Definition:
    # define some constants
    COLUMNS_NEEDED: dict[str, str] = {
        "latitude": "Latitude",
        "longitude": "Longitude",
        "chargedeviceid": "Charge Device ID",
        "name": "Name",
        "town": "Town",
        "street": "Street",
        "county": "County",
        "postcode": "Postcode",
        "access24hours": "24-hour Access",
        "paymentrequired": "Payment Required",
        "subscriptionrequired": "Subscription Required",
        "accessrestrictionflag": "Restricted Access",
        "parkingfeesflag": "Parking Fees Required",
        "locationtype": "Location Type",
        "devicemanufacturer": "Device Manufacturer",
        "deviceownername": "Device Owner",
        "chargedevicestatus": "Device Status",
        "devicecontrollername": "Device Controller",
        "connector1type": "Connector 1 Type",
        "connector1chargemethod": "Connector 1 Charge Method",
        "connector1chargemode": "Connector 1 Charge Mode",
        "connector1tetheredcable": "Connector 1 Tethered Cable",
        "connector1status": "Connector 1 Status",
        "connector1ratedoutputkw": "Connector 1 Rated Output (kW)",
        "connector1outputcurrent": "Connector 1 Output Current (A)",
        "connector1ratedvoltage": "Connector 1 Rated Voltage (V)",
        "connector2type": "Connector 2 Type",
        "connector2chargemethod": "Connector 2 Charge Method",
        "connector2chargemode": "Connector 2 Charge Mode",
        "connector2tetheredcable": "Connector 2 Tethered Cable",
        "connector2status": "Connector 2 Status",
        "connector2ratedoutputkw": "Connector 2 Rated Output (kW)",
        "connector2outputcurrent": "Connector 2 Output Current (A)",
        "connector2ratedvoltage": "Connector 2 Rated Voltage (V)",
        "connector3type": "Connector 3 Type",
        "connector3chargemethod": "Connector 3 Charge Method",
        "connector3chargemode": "Connector 3 Charge Mode",
        "connector3tetheredcable": "Connector 3 Tethered Cable",
        "connector3status": "Connector 3 Status",
        "connector3ratedoutputkw": "Connector 3 Rated Output (kW)",
        "connector3outputcurrent": "Connector 3 Output Current (A)",
        "connector3ratedvoltage": "Connector 3 Rated Voltage (V)",
    }

    MISSPELT_COUNTY_NAMES: dict[str, str] = {
        "Essesx": "Essex",
        "Argyl and Bute": "Argyll and Bute",
        "Argyll": "Argyll and Bute",
        "Lond": "London",
    }

    WRONG_LAT_LONG: dict[str, list[float]] = dict(
        zip(
            [
                "Breer Street, United Kingdom",
                "Hale End Road, E17 4DJ, United Kingdom",
                "Alverstone Road 2, Coventory, CV2 4QE, United Kingdom",
                "57 Queen's Gate, SW7 5JW, United Kingdom",
                "Bagleys Lane, United Kingdom",
                "Sway, Lymington, SO41 6AE, United Kingdom",
                "Copley Park, London SW16 3DE",
                "Temple Road, London NW2 6PJ",
            ],
            [
                [51.466588, 51.466588],
                [51.595946, 51.595946],
                [-1.485505, 52.416177],
                [-0.179309, 51.496127],
                [0, 0],
                [5, 4.999684],
                [51.420576, 51.420576],
                [51.559976, 51.559976],
            ],
        )
    )

    DISTANCE_THRESHOLD: float = 25.0
    CONNECTOR_LABELS = ["Connector 1", "Connector 2", "Connector 3"]
    TAB_NAMES: dict[str, list] = {
        "Accessibility": [
            "24-hour Access",
            "Payment Required",
            "Subscription Required",
            "Restricted Access",
            "Parking Fees Required",
        ],
        "Demography": [
            "Town",
            "County",
            "Location Type",
        ],
        "Ownership": [
            "Device Manufacturer",
            "Device Owner",
            "Device Controller",
        ],
        "Connector 1": [
            "Connector 1 Rated Output (kW)",
            "Connector 1 Output Current (A)",
            "Connector 1 Rated Voltage (V)",
        ],
        "Connector 2": [
            "Connector 2 Rated Output (kW)",
            "Connector 2 Output Current (A)",
            "Connector 2 Rated Voltage (V)",
        ],
        "Connector 3": [
            "Connector 3 Rated Output (kW)",
            "Connector 3 Output Current (A)",
            "Connector 3 Rated Voltage (V)",
        ],
    }
