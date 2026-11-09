// Content-only substitutions. Original variant transitions and scroll controller are untouched.
export function customizeSticky(source) {
 const copy = {
 'Less noise. More focus.':'Every set, recorded.', 'More clarity. More flow.':'Your history, together.',
 'Work better together.':'See what adds up.', 'Build better together.':'Your training, in view.',
 'View your progress.':'See the bigger picture.', 'Find your next step.':'Across muscle groups.',
 'Bring projects and priorities into one clear space. Keep your next steps focused and easy to follow. Turn scattered plans into steady, lasting progress.':'Review the weights and reps from each session, with personal records alongside your workout history.',
 'Keep your ideas and conversations in one place. Share clear context and give valuable feedback. Turn a shared direction into confident decisions.':'Review training volume, recent sessions and personal records in your strength overview.',
 'See your progress and what needs focus now. Bring priorities and team workload into focus. Find the clarity to make your next move easier.':'Explore your training across muscle groups, with volume, sessions and load views.'
 };
 for (const [from,to] of Object.entries(copy)) source=source.split(from).join(to);
 for (const [id,file] of Object.entries({BRqgFFbvLw3ilMXnPVonIGrXOQ:'workout-history.png','12yzuMWOuyhMq2pXyVdNjPIBj0':'strength.png','6JRVxrWi9g9CAdumAYN3Bdew':'muscle-balance.png'})) {
  source=source.replace(new RegExp('https://framerusercontent.com/images/'+id+'\\.png[^" ]*','g'),'/assets/product/'+file);
 }
 // One local capture per image instead of mismatched template responsive sizes.
 source=source.replace(/srcSet:"[^"]*"/g,'srcSet:undefined');
 source=source.replace('anchor:50,anchorMode:"preview"','anchor:typeof window!=="undefined"&&window.innerWidth<=700?78:50,anchorMode:typeof window!=="undefined"&&window.innerWidth<=700?"viewport":"preview"');
 return source;
}
