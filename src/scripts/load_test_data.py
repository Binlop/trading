# scripts/load_test_data.py
import asyncio
from pathlib import Path

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from db.session import LocalSession
from spimex.models import PetroleumProducts  # noqa: F401
from sqlalchemy import insert


async def load_csv(session: AsyncSession):
    csv_path = Path(__file__).parent / "pdf_final_df.csv"
    df = pd.read_csv(csv_path, sep="\t")
    df["date"] = pd.to_datetime(df["date"]).dt.to_pydatetime()
    df["delivery_basis_name"] = df["delivery_basis_name"].fillna("НЕИЗВЕСТНО")
    rows = df.to_dict(orient="records")

    chunk_size = 5000
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i:i + chunk_size]
        await session.execute(insert(PetroleumProducts), chunk)
        await session.commit()

async def main() -> None:
    async with LocalSession() as session:
        await load_csv(session)

if __name__ == "__main__":
    asyncio.run(main())