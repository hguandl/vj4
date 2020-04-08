from vj4 import app
from vj4.handler import base
from vj4.util import misc
from vj4.model import record

from datetime import datetime

@app.route('/about', 'about', global_route=True)
class AboutHandler(base.Handler):
  async def get(self):
    self.render('about.html')


@app.route('/wiki/help', 'wiki_help', global_route=True)
class AboutHandler(base.Handler):
  async def get(self):
    self.render('wiki_help.html')


@app.route('/preview', 'preview', global_route=True)
class PreviewHandler(base.Handler):
  @base.post_argument
  @base.sanitize
  async def post(self, *, text: str):
    self.response.content_type = 'text/html'
    self.response.text = misc.markdown(text)


@app.route('/status/waiting', 'status', global_route=True)
class WaitingStatusHandler(base.Handler):
  async def get(self):
    waiting_records = []
    waiting = record.get_multi(get_hidden=True, status={'$eq': 0})\
                    .sort('judge_at', -1)\
                    .limit(5)
    async for r in waiting:
      waiting_records.append(r['judge_at'])
    last_waiting_time = waiting_records[0] if len(waiting_records) > 0 else 0

    now = datetime.now()
    if len(waiting_records) >= 5 or now.timestamp() - last_waiting_time <= 300:
      should_restart = True
    else:
      should_restart = False

    resp = {
      'waiting_count': len(waiting_records),
      'last_waiting_time': last_waiting_time,
      'should_restart': should_restart
    }
    self.json(resp)
