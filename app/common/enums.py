from enum import Enum


class JobSource(str, Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    NAUKRI = "naukri"
    WELLFOUND = "wellfound"
    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    REMOTEOK = "remoteok"
    ARBEITNOW = "arbeitnow"
    MANUAL = "manual"


class ApplicationStatus(str, Enum):
    SAVED = "saved"
    APPLIED = "applied"
    REJECTED = "rejected"
    INTERVIEWING = "interviewing"
    OFFERED = "offered"