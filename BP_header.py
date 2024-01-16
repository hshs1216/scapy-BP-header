BP_header = {
    # Primary Header
    "version": {"value": 0x06, "digits": 2},
    "BPCF": {"value": 0x10, "digits": 2},
    "Bundle Header Length": {"value": 0x17, "digits": 2},
    "Destination Scheme Offset": {"value": 0x01, "digits": 2},
    "Destination SSP Offset": {"value": 0x01, "digits": 2},
    "Source Scheme Offset": {"value": 0x01, "digits": 2},
    "Source SSP Offset": {"value": 0x02, "digits": 2},
    "Report Scheme Offset": {"value": 0x01, "digits": 2},
    "Report SSP Offset": {"value": 0x02, "digits": 2},
    "Custodian Scheme Offset": {"value": 0x00, "digits": 2},
    "Custodian SSP Offset": {"value": 0x00, "digits": 2},
    "Timestamp":{"value": 0x82e8ffcc3a, "digits": 10},
    "Timestamp Sequence Number":  {"value": 0x01, "digits": 2},
    "Lifetime": {"value": 0x9c10, "digits": 4},
    "Dictionary Length": {"value": 0x00, "digits": 2},

    # #Extention Block
    # "Block Type Code": {"value": 0x05, "digits": 2},
    # "Block Processing Control Flags":  {"value": 0x10, "digits": 2},
    # "Block Length":  {"value": 0x08, "digits": 2},
    # "Previous Hop Scheme":  {"value": 0x69706e00, "digits": 8},
    # "Previous Hop EID":  {"value": 0x312e3000, "digits": 8},

    # #Extention Block
    # "Block Type Code: Bundle Age Extension Block": {"value": 0x14, "digits": 2},
    # "Block Processing Control Flags 2":  {"value": 0x01, "digits": 2},
    # "Block Length 2": {"value": 0x01, "digits": 2},
    # "Bundle Age in seconds":  {"value": 0x00, "digits": 2},
    
    #Payload Block
    "Payload Header": {"value": 0x010940, "digits": 6},
    "Payload Data1": {"value": 0x010940332031373033373530303734203532303935392038383134206270696e672,
                     "digits": 32},
    "Payload Data2": {"value": 0x07061796c6f61640000000000000000000000000000000000000000000000000000, 
                    "digits": 32}
}

