// Content-only substitutions. Original variant transitions and scroll controller are untouched.
export function customizeSticky(source) {
 const copy = {
 'Less noise. More focus.':'Your previous sessions.', 'More clarity. More flow.':'Ready to revisit.',
 'Work better together.':'Follow your volume.', 'Build better together.':'Across your training.',
 'View your progress.':'See your muscle groups.', 'Find your next step.':'Across your sessions.',
 'Bring projects and priorities into one clear space. Keep your next steps focused and easy to follow. Turn scattered plans into steady, lasting progress.':'Look back at the weights and reps you recorded in each workout.',
 'Keep your ideas and conversations in one place. Share clear context and give valuable feedback. Turn a shared direction into confident decisions.':'Review your training volume and personal records in the strength overview.',
 'See your progress and what needs focus now. Bring priorities and team workload into focus. Find the clarity to make your next move easier.':'Explore your training across muscle groups, with volume, sessions and load views.'
 };
 for (const [from,to] of Object.entries(copy)) source=source.split(from).join(to);
 for (const [id,file] of Object.entries({BRqgFFbvLw3ilMXnPVonIGrXOQ:'workout-history.webp','12yzuMWOuyhMq2pXyVdNjPIBj0':'strength.webp','6JRVxrWi9g9CAdumAYN3Bdew':'muscle-balance.webp'})) {
  source=source.replace(new RegExp('https://framerusercontent.com/images/'+id+'\\.png[^" ]*','g'),'/assets/product/'+file);
 }
 // One local capture per image instead of mismatched template responsive sizes.
 source=source.replace(/srcSet:"[^"]*"/g,'srcSet:undefined');
 source=source.replace('anchor:50,anchorMode:"preview"','anchor:typeof window!=="undefined"&&window.innerWidth<=700?78:50,anchorMode:typeof window!=="undefined"&&window.innerWidth<=700?"viewport":"preview"');
 return source;
}
