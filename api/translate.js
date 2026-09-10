// POST { task, ask } -> { spec }
// Key lives in a Vercel environment variable, never in the client bundle.
const SYSTEM = {
  'spec': `You are a senior solutions architect. Turn the business ask into a concise first-draft technical spec.
Use exactly these headings, each on its own line, plain text only, no markdown symbols:
SYSTEMS TOUCHED / TRIGGER / DATA FLOW / FIELD MAPPING / EDGE CASES.
Be specific and terse. Under 220 words.`,

  'gap-agent': `You are an implementation review agent. The user describes how a customer configured their account.
Return a prioritized list of gaps. For each: the issue, a severity of HIGH, MEDIUM or LOW, and the specific recommended fix.
Order by severity. Plain text, no markdown symbols. Under 200 words.`,

  'colleague-agent': `You are an internal team assistant for a solutions architecture team.
Answer the request directly and practically, as if you had access to the team's account and activity data.
Where you would need real data, name the specific source you would pull it from. Plain text. Under 180 words.`,

  'board-narrative': `You are drafting the narrative paragraph of a monthly business update from the metrics given.
Explain what the numbers mean together, and call out anything that would need a story from the executive.
Neutral, factual, no hype. Plain text. Under 150 words.`,

  'meeting-actions': `Extract action items from the meeting notes.
For each: the owner, the action, and the due date if one is stated. If no owner is named, write OWNER UNASSIGNED.
Ignore general discussion that carries no commitment. Plain text, one item per line. Under 150 words.`,

  'health-summary': `You are advising a customer success manager before a renewal conversation.
From the account health score and signals given, write the specific talking points to bring into the call and the one action to take this week.
Concrete, not generic. Plain text. Under 150 words.`
};

let resolvedModel = null;

module.exports = async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const key = process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_API_KEY || process.env.ANTHROPIC_KEY;
  if (!key) return res.status(500).json({ error: 'API key not configured' });

  try {
    const { task, ask } = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    const system = SYSTEM[task] || SYSTEM['spec'];
    if (!ask || !String(ask).trim()) return res.status(400).json({ error: 'Empty input' });

    // Model availability differs per account, so try the cheap ones first and
    // remember whichever works for the life of this warm instance.
    const candidates = process.env.CLAUDE_MODEL
      ? [process.env.CLAUDE_MODEL]
      : ['claude-haiku-4-5', 'claude-3-5-haiku-20241022', 'claude-3-5-haiku-latest',
         'claude-sonnet-4-5', 'claude-3-5-sonnet-20241022'];
    const order = resolvedModel ? [resolvedModel, ...candidates.filter(m => m !== resolvedModel)] : candidates;

    let r = null, lastDetail = '';
    for (const model of order) {
      r = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'content-type': 'application/json',
          'x-api-key': key,
          'anthropic-version': '2023-06-01'
        },
        body: JSON.stringify({
          model,
          max_tokens: 400,
          system,
          messages: [{ role: 'user', content: String(ask).slice(0, 1200) }]
        })
      });
      if (r.ok) { resolvedModel = model; break; }
      lastDetail = await r.text();
      // only a missing model is worth retrying; anything else is a real failure
      if (!lastDetail.includes('not_found_error')) break;
    }

    if (!r || !r.ok) {
      return res.status(502).json({ error: 'Upstream error', detail: lastDetail.slice(0, 300) });
    }

    const data = await r.json();
    const spec = (data.content || []).map(b => b.text || '').join('').trim();
    if (!spec) return res.status(502).json({ error: 'Empty response' });
    return res.status(200).json({ spec });
  } catch (err) {
    return res.status(500).json({ error: 'Request failed', detail: String(err).slice(0, 200) });
  }
};
