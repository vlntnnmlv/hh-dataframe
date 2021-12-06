import pickle
import pandas as pd
import re

def toDataFrame(raw_data=None, filename=None):
    if filename:
        with open(filename, "rb") as inp:
            unpickler = pickle.Unpickler(inp)
            raw_data = unpickler.load()

    df = pd.DataFrame(raw_data)

    # change inclusive fields
    df.experience = df.experience.apply(lambda x : x['id'])
    df.billing_type = df.billing_type.apply(lambda x : x['id'])
    df.schedule = df.schedule.apply(lambda x : x['id'])
    df.key_skills = df.key_skills.apply(lambda x : [e['name'] for e in x] if x else None)

    df['city'] = df.address.apply(lambda x : x['city'] if x else None)
    df['metro'] = df.address.apply(lambda x : x['metro']['station_name'] if x and x['metro'] else None)
    df.address = df.address.apply(lambda x : x['raw'] if x else None)
    df.employment = df.employment.apply(lambda x : x['id'] if x else None)

    df['min_salary'] = df.salary.apply(lambda x : x['from'] if x else None)
    df['max_salary'] = df.salary.apply(lambda x : x['to'] if x else None)
    df['gross'] = df.salary.apply(lambda x : x['gross'] if x else None)
    df['currency'] = df.salary.apply(lambda x : x['currency'] if x else 'RUR')
    df.employer = df.employer.apply(lambda x : x['name'] if x else None)
    df.type = df.type.apply(lambda x : x['id'] if x else None)
    df.specializations = df.specializations.apply(lambda x : [e['id'] for e in x])
    df.working_days = df.working_days.apply(lambda x : [e['id'] for e in x] if x else None)
    df.working_time_intervals = df.working_time_intervals.apply(lambda x : [e['id'] for e in x] if x else None)
    df.working_time_modes = df.working_time_modes.apply(lambda x : [e['id'] for e in x] if x else None)

    df['professional_role'] = df.professional_roles.apply(lambda x : [e['id'] for e in x] if x else None)
    df.description = df.description.apply(lambda x : re.sub(re.compile('<.*?>|;|,'), '', x) if x else None)
    
    df.driver_license_types = df.driver_license_types.apply(lambda x : [e['id'] for e in x] if x else None)
    
    df.index = df.id
    # drop odd columns
    df = df.drop(
        [
            "id",
            "test",
            "area",
            "code",
            "hidden",
            "premium",
            "contacts",
            "relations",
            "department",
            "allow_messages",
            "insider_interview",
            "professional_roles",
            "immediate_redirect_url",
            "quick_responses_allowed",
            "branded_description",
            "suitable_resumes_url",
            "apply_alternate_url",
            "negotiations_url",
            "alternate_url",
            "response_url",
            "salary",
            "site"
            ],
                axis=1)

    return df