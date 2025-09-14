const fs = require('fs');

const boards = ['MMA90mFH', 'rbISqlOt'];
const key = process.env.TRELLO_KEY;
const token = process.env.TRELLO_TOKEN;

if (!key || !token) {
  console.error('Missing Trello credentials');
  process.exit(1);
}

async function fetchBoard(boardId) {
  const url = `https://api.trello.com/1/boards/${boardId}/lists?cards=open&card_fields=name,desc,url,labels&fields=name&key=${key}&token=${token}`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to fetch board ${boardId}`);
  }
  return res.json();
}

async function main() {
  const data = {};
  for (const boardId of boards) {
    const lists = await fetchBoard(boardId);
    const matchingLists = lists.filter(list => list.name.toLowerCase().includes('docket'));
    const cards = matchingLists.flatMap(list => list.cards || []);
    data[boardId] = cards;
  }
  fs.writeFileSync('assets/docket-fallback.json', JSON.stringify(data, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
