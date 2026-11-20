import { copyFileSync, mkdirSync } from "node:fs";

const here = new URL(".", import.meta.url);
const source = new URL("entry.png", here);
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });
copyFileSync(source, new URL("entry.png", `file://${outputDir.replace(/\/$/, "")}/`));
