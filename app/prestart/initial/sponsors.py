import pandas as pd
from sqlmodel import Session, select

from app.core.db import engine, old_engine
from app.features.companies.model import Company


def load_old_sponsor_data() -> pd.DataFrame:
    """Load old sponsor data from a CSV file."""

    df = pd.read_sql("SELECT * FROM sponsors", con=old_engine)
    return df


def load_sponsor_data():
    with Session(engine) as session:
        existing_sponsors = session.exec(select(Company)).first()
        if existing_sponsors:
            logger.info("Sponsor data already exists, skipping initialization")
            return
        sponsor_data = load_old_sponsor_data().unique("sp_company")

        sponsors = sponsor_data["sp_company"].unique().tolist()

        for sponsor in sponsors:
            company = Company(
                name=sponsor,
                sponsoring=True,
            )
            session.add(company)
        session.commit()
    logger.info("Sponsor data loaded successfully")
    return


if __name__ == "__main__":
    data = load_sponsor_data()
