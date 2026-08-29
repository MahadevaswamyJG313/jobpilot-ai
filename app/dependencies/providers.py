from app.providers import RemoteOKProvider, LinkedInProvider, ArbeitnowProvider, MultiJobProvider


def get_job_provider():
    return MultiJobProvider([
        RemoteOKProvider(),
        LinkedInProvider(),
        ArbeitnowProvider(),
    ])