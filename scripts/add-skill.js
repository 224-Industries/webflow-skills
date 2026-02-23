#!/usr/bin/env node

/**
 * @module add-skill
 * @description Scaffolds a new skill directory with a SKILL.md template, then
 * runs sync-skills.js to register it across all generated files.
 * @param {string} skill-name - Name of the skill (normalized to lowercase with hyphens).
 * @param {string} description - Brief description of what the skill does.
 * @example
 * node scripts/add-skill.js my-new-skill "Helps with X tasks"
 */

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = join(__dirname, "..");
const SKILLS_DIR = join(ROOT_DIR, "skills");
const MANIFEST_PATH = join(ROOT_DIR, "manifest.json");
const SYNC_SCRIPT = join(__dirname, "sync-skills.js");

function normalizeName(input) {
  return input
    .toLowerCase()
    .trim()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9-]/g, "")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function printUsage() {
  console.log(`
Usage: node scripts/add-skill.js <skill-name> <description>

Arguments:
  skill-name   Name of the skill (will be normalized to lowercase with hyphens)
  description  Brief description of what the skill does

Example:
  node scripts/add-skill.js my-new-skill "Helps with data processing tasks"
`);
}

// Reads and parses manifest.json, exiting with an error
// if the file is missing or malformed.
async function loadManifest() {
  try {
    const content = await readFile(MANIFEST_PATH, "utf-8");
    return JSON.parse(content);
  } catch {
    console.error("Error: Could not read manifest.json");
    console.error("Make sure you're running this from the repository root.");
    process.exit(1);
  }
}

// Checks whether a skill directory with a SKILL.md already exists,
// returning true if so to prevent overwriting.
async function skillExists(skillName) {
  try {
    await readFile(join(SKILLS_DIR, skillName, "SKILL.md"), "utf-8");
    return true;
  } catch {
    return false;
  }
}

// Returns a SKILL.md template string with frontmatter populated
// from the given skill name, description, and manifest metadata.
function generateSkillMd(skillName, description, manifest) {
  const author = manifest.author?.name || "224 Industries";
  const license = manifest.license || "MIT";

  return `---
name: ${skillName}
description: ${description}
license: ${license}
metadata:
  author: ${author}
  version: "1.0.0"
  keywords: "ai, agent, skill"
---

`;
}

// Spawns sync-skills.js as a child process so the new skill
// is registered in manifest.json, plugins, and README.
async function runSyncScript() {
  const { spawn } = await import("node:child_process");

  return new Promise((resolve, reject) => {
    const child = spawn("node", [SYNC_SCRIPT], {
      stdio: "inherit",
      cwd: ROOT_DIR,
    });

    child.on("close", (code) => {
      if (code === 0) {
        resolve();
      } else {
        reject(new Error(`sync-skills.js exited with code ${code}`));
      }
    });

    child.on("error", reject);
  });
}

// Entry point — validates CLI args, scaffolds the skill directory
// with a SKILL.md template, then runs sync-skills.js.
async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2 || args.includes("--help") || args.includes("-h")) {
    printUsage();
    process.exit(args.includes("--help") || args.includes("-h") ? 0 : 1);
  }

  const [rawName, ...descParts] = args;
  const description = descParts.join(" ");
  const skillName = normalizeName(rawName);

  if (!skillName) {
    console.error(
      "Error: Skill name must contain at least one letter or number"
    );
    process.exit(1);
  }

  if (!description) {
    console.error("Error: Description is required");
    process.exit(1);
  }

  if (await skillExists(skillName)) {
    console.error(`Error: Skill "${skillName}" already exists`);
    process.exit(1);
  }

  console.log(`\nCreating skill: ${skillName}\n`);

  const manifest = await loadManifest();
  const skillDir = join(SKILLS_DIR, skillName);

  await mkdir(skillDir, { recursive: true });

  const skillMd = generateSkillMd(skillName, description, manifest);
  await writeFile(join(skillDir, "SKILL.md"), skillMd, "utf-8");

  console.log(`Created skills/${skillName}/SKILL.md`);
  console.log();

  console.log("Running sync-skills.js...\n");
  await runSyncScript();

  console.log(`\nSkill "${skillName}" created successfully!`);
  console.log("\nNext steps:");
  console.log(
    `  1. Edit skills/${skillName}/SKILL.md to add your skill content`
  );
  console.log(
    `  2. Add keywords to the SKILL.md frontmatter for better discoverability`
  );
  console.log();
}

main().catch((error) => {
  console.error("Error:", error.message);
  process.exit(1);
});
