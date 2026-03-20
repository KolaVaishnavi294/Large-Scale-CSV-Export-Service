import csv

async def stream_export(pool, job, filepath, filters, columns, delimiter, quotechar):

    job.status = "processing"

    base_query = f"SELECT {','.join(columns)} FROM users"

    conditions = []
    params = []

    if filters.get("country_code"):
        conditions.append("country_code = $1")
        params.append(filters["country_code"])

    if filters.get("subscription_tier"):
        conditions.append("subscription_tier = $2")
        params.append(filters["subscription_tier"])

    if filters.get("min_ltv"):
        conditions.append("lifetime_value >= $3")
        params.append(filters["min_ltv"])

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    async with pool.acquire() as conn:

        job.total_rows = await conn.fetchval("SELECT COUNT(*) FROM users")

        offset = 0
        chunk_size = 1000

        with open(filepath, "w", newline="") as f:

            writer = csv.writer(
                f,
                delimiter=delimiter,
                quotechar=quotechar
            )

            writer.writerow(columns)

            while True:

                query = base_query + f" LIMIT {chunk_size} OFFSET {offset}"

                rows = await conn.fetch(query)

                if not rows:
                    break

                for r in rows:
                    writer.writerow(list(r))

                offset += chunk_size
                job.processed_rows += len(rows)

    job.status = "completed"