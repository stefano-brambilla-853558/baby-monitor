class Keys:
    DIAPERS = "diapers"
    CONTRACTION = "contraction"
    CONTRACTION_PRIMARY = "contractions_primary"


data_files = {
    Keys.DIAPERS: "diapers.csv",
    Keys.CONTRACTION: "contractions.csv"
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
    ]
}