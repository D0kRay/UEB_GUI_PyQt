class data_content:

    # GUI_id = int
    # DT_id = int
    # Status_Byte = bytearray
    # MaxPackages = int
    # Count = int
    # StatusPacket = bool
    # Data = list
    # DataFetched = bool

    def __init__(self):
        self.GUI_id = -1
        self.DT_id = -1
        self.Status_Byte = 0
        self.MaxPackages = -1
        self.Count = -1
        self.StatusPacket = False
        self.Data = []
        self.DataFetched = False

    