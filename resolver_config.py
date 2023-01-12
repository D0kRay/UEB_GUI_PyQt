class ResolverConfig:

    # los_thres = float
    # dos_overrange_thres = float
    # dos_mismatch_thres = float
    # dos_reset_max_thres = float
    # dos_reset_min_thres = float
    # lot_high_thres = float
    # lot_low_thres = float
    # excitation_frequency = float
    # phase_lock_range = bool
    # hysteresis = bool
    # encoder_resolution = int
    # rdc_resolution = int

        def __init__(self):
            self.los_thres = 0.0000
            self.dos_overrange_thres = 4.826
            self.dos_mismatch_thres = 4.826
            self.dos_reset_max_thres = 0.038
            self.dos_reset_min_thres = 4.788
            self.lot_high_thres = 9.017
            self.lot_low_thres = 9.017
            self.excitation_frequency = 10000
            self.phase_lock_range = False
            self.hysteresis = True
            self.encoder_resolution = 16
            self.rdc_resolution = 16
