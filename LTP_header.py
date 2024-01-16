LTP_header = {

    #LTP Header
        #Version
        "LTP Version":              {"value": 0x0, "digits": 1},
        "LTP Type":                 {"value": 0x3, "digits": 1}, #Red data, Checkpoint, EORP, EOB
        #Session Name
        "Session originator":       {"value": 0x01, "digits": 2},
        "Session number":           {"value": 0x03, "digits": 2},
        #Header Extention
        "Header Extension Count":   {"value": 0x0, "digits": 1},
        "Trailer Extension Count":  {"value": 0x0, "digits": 1},
    #Data Segment
        "Client service ID":        {"value": 0x01, "digits": 2}, #01 = Bundle Protocol
        "Offset":                   {"value": 0x00, "digits": 2},
        "Length":                   {"value": 0x49, "digits": 2},
        "Checkpoint serial number": {"value": 0x927a, "digits": 4},
        "Report serial number":     {"value": 0x00, "digits": 2},
}

# SEGMENT TYPE CODE
#    CTRL EXC Flag1  Flag0  Code  Nature of segment
#    ---- --- ------ ------ ----  ---------------------------------------
#      0   0     0      0     0   Red data, NOT {Checkpoint, EORP or EOB}
#      0   0     0      1     1   Red data, Checkpoint, NOT {EORP or EOB}
#      0   0     1      0     2   Red data, Checkpoint, EORP, NOT EOB
#      0   0     1      1     3   Red data, Checkpoint, EORP, EOB
#      0   1     0      0     4   Green data, NOT EOB
#      0   1     1      1     7   Green data, EOB
#      1   0     0      0     8   Report segment

# Red
# The block prefix that is to be transmitted reliably, 
# i.e., subject to acknowledgment and retransmission.

# Green
# The block suffix that is to be transmitted unreliably, 
# i.e., not subject to acknowledgments or retransmissions.
# If present, the green-part of a block begins at the octet following the end of the red-part.

# EOB
# The last data segment transmitted as part of the original transmission of a block.

# EORB
# The segment transmitted as part of the original transmission of a block containing 
# the last octet of the block's red-part.

