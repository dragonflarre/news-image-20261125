// The Daily Compass, Wednesday 25 November 2026: the front page is drawn by
// make_paper.py and committed as entry.png; this program copies it to the
// output directory the harness names.

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outputDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), target);
console.log('wrote', target);
