// Content-only substitutions. Original variant transitions and scroll controller are untouched.
export function customizeIngredients(source) {
 const copy = {
 'Less noise. More focus.':'Add what a photo misses.', 'More clarity. More flow.':'Before the estimate.',
 'Work better together.':'Understand the grade.', 'Build better together.':'Look at the ingredients.',
 'View your progress.':'Review before you log.', 'Find your next step.':'Make it your serving.',
 'Bring projects and priorities into one clear space. Keep your next steps focused and easy to follow. Turn scattered plans into steady, lasting progress.':'Add oil, butter, sauces or other extras, and choose a portion size before estimating your meal.',
 'Keep your ideas and conversations in one place. Share clear context and give valuable feedback. Turn a shared direction into confident decisions.':'Review ingredient flags, positive findings and the explanation behind a product’s COR grade.',
 'See your progress and what needs focus now. Bring priorities and team workload into focus. Find the clarity to make your next move easier.':'Check the calories, macros and serving size. Make changes before saving.'
 };
 for (const [from,to] of Object.entries(copy)) source=source.split(from).join(to);
 for (const [id,file] of Object.entries({BRqgFFbvLw3ilMXnPVonIGrXOQ:'questions.webp','12yzuMWOuyhMq2pXyVdNjPIBj0':'ingredients.webp','6JRVxrWi9g9CAdumAYN3Bdew':'nutrition.webp'})) {
  source=source.replace(new RegExp('https://framerusercontent.com/images/'+id+'\\.png[^" ]*','g'),'/assets/product/'+file);
 }
 // One local capture per image instead of mismatched template responsive sizes.
 source=source.replace(/srcSet:"[^"]*"/g,'srcSet:undefined');
 source=source.replace('anchor:50,anchorMode:"preview"','anchor:typeof window!=="undefined"&&window.innerWidth<=700?78:50,anchorMode:typeof window!=="undefined"&&window.innerWidth<=700?"viewport":"preview"');
 return source;
}
