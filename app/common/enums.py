from enum import Enum


class JobSource(str, Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    NAUKRI = "naukri"
    WELLFOUND = "wellfound"
    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    REMOTEOK = "remoteok"
    MANUAL = "manual"