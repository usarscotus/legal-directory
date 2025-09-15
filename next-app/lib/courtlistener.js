const API_BASE = 'https://www.courtlistener.com/api/rest/v3';

const headers = {
  'Authorization': `Token ${process.env.NEXT_PUBLIC_CL_API_KEY}`,
};

export async function searchOpinions(query) {
  const url = `${API_BASE}/search/?type=o&court=scotus&q=${encodeURIComponent(query)}&page_size=10`;
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error('Search failed');
  const data = await res.json();
  return data.results || [];
}

export async function getOpinion(id) {
  const url = `${API_BASE}/opinions/${id}/?fields=id,case_name,citation,date_filed,cites,cited_by`; // may return cites arrays
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error('Opinion fetch failed');
  return res.json();
}

export async function getOpinionsByUris(uris = []) {
  const ids = uris
    .map((uri) => uri.match(/\/opinions\/(\d+)/)?.[1])
    .filter(Boolean)
    .join(',');
  if (!ids) return [];
  const url = `${API_BASE}/opinions/?id__in=${ids}&fields=id,case_name,citation,date_filed`;
  const res = await fetch(url, { headers });
  if (!res.ok) throw new Error('Related opinions fetch failed');
  const data = await res.json();
  return data.results || [];
}
