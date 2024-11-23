class Keys:
    DIAPERS = "diapers"
    CONTRACTION = "contraction"
    CONTRACTION_PRIMARY = "contractions_primary"
    NAPS = "naps"
    FEEDING = "feeding"
    CRY = "cry"


data_files = {
    Keys.DIAPERS: "diapers.csv",
    Keys.CONTRACTION: "contractions.csv",
    Keys.NAPS: "naps.csv",
    Keys.FEEDING: "feeding.csv",
    Keys.CRY: "cry.csv"
}

data_columns = {
    Keys.DIAPERS: [
        "Timestamp",
        "Content",
        "Note",
        "Metadata"
    ],
    Keys.CONTRACTION: [
        "Timestamp",
        "Type",
        "Intensity",
        "Note"
    ],
    Keys.CONTRACTION_PRIMARY: [
        "ID",
        "Timestamp_start",
        "Timestamp_end",
        "Duration",
        "Time_between",
        "Intensity",
        "Note"
    ],
    Keys.NAPS: [
        "Timestamp",
        "Type",
        "Note"
    ],
    Keys.FEEDING: [
        "Timestamp",
        "Type",
        "Quantity",
        "Note"
    ],
    Keys.CRY: [
        "Timestamp",
        "Filename",
        "Note"
    ]

}