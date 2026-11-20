// gta6-meme-x-01 — entry program for make.fun's "Post a GTA 6 meme on X"
// bounty. The entry itself is the X post whose address lives in
// POST.json; this program copies that file into the grader's output
// directory, exactly the way the kit's harness runs it:
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// No network, no secrets, no side effects beyond the one copy.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, "POST.json"), join(outDir, "POST.json"));
