import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Copy the rendered front page next to the output folder the harness
// expects. Node 22 standard library only; no network, no dependencies.
const scriptDir = dirname(fileURLToPath(import.meta.url));
const source = join(scriptDir, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(source, target);
console.log(target);
