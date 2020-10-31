import asyncio

from vj4.model import record
from vj4 import db
from vj4.util import options

async def main():
  options.db_name = 'adoj'
  await db.init()
  records = record.get_multi(get_hidden=True, pid={'$eq': 1024})
  targets = []
  async for r in records:
    targets.append(r['_id'])

  for t in targets:
    print(t)
    await record.rejudge(t)


if __name__ == "__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
