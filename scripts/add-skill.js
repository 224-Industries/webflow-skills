#!/usr/bin/env node

/**
 * add-skill.js
 *
 * Adds a new skill to the repository.
 *
 * Usage: node scripts/add-skill.js <skill-name> <description>
 *
 * Example: node scripts/add-skill.js my-new-skill "Helps with X tasks"
 */

import { mkdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = join(__dirname, "..");
const SKILLS_DIR = join(ROOT_DIR, "skills");
const MARKETPLACE_PATH = join(ROOT_DIR, ".claude-plugin", "marketplace.json");
const SYNC_SCRIPT = join(__dirname, "sync-skills.js");

const SKILLS_SUFFIX_REGEX = /-skills$/;

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

async function loadMarketplace() {
  try {
    const content = await readFile(MARKETPLACE_PATH, "utf-8");
    return JSON.parse(content);
  } catch {
    console.error("Error: Could not read .claude-plugin/marketplace.json");
    console.error("Make sure you're running this from the repository root.");
    process.exit(1);
  }
}

async function skillExists(skillName) {
  try {
    await readFile(join(SKILLS_DIR, skillName, "SKILL.md"), "utf-8");
    return true;
  } catch {
    return false;
  }
}

function generateSkillMd(skillName, description, marketplace) {
  const brandName = marketplace.name.replace(SKILLS_SUFFIX_REGEX, "");
  const license =
    marketplace.plugins?.[0]?.license || marketplace.license || "MIT";

  return `---
name: ${skillName}
description: ${description}
license: ${license}
metadata:
  author: ${brandName}
  version: "1.0.0"
---

`;
}

function generatePluginJson(skillName, description, marketplace) {
  const owner = marketplace.owner || {};
  const existingPlugin = marketplace.plugins?.[0] || {};

  return JSON.stringify(
    {
      name: skillName,
      description,
      version: "1.0.0",
      author: {
        name: owner.name || "Your Name",
        email: owner.email || "your.email@example.com",
      },
      license: existingPlugin.license || "MIT",
      homepage: existingPlugin.homepage || "https://example.com",
      repository: existingPlugin.repository || "",
      keywords: existingPlugin.keywords || "ai, agent, skill",
      category: existingPlugin.category || "general",
    },
    null,
    2
  );
}

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

  const marketplace = await loadMarketplace();
  const skillDir = join(SKILLS_DIR, skillName);
  const pluginDir = join(skillDir, ".claude-plugin");

  // Create directories
  await mkdir(pluginDir, { recursive: true });

  // Generate files
  const skillMd = generateSkillMd(skillName, description, marketplace);
  const pluginJson = generatePluginJson(skillName, description, marketplace);

  await writeFile(join(skillDir, "SKILL.md"), skillMd, "utf-8");
  await writeFile(join(pluginDir, "plugin.json"), `${pluginJson}\n`, "utf-8");

  console.log(`✓ Created skills/${skillName}/SKILL.md`);
  console.log(`✓ Created skills/${skillName}/.claude-plugin/plugin.json`);
  console.log();

  // Run sync script
  console.log("Running sync-skills.js...\n");
  await runSyncScript();

  console.log(`\nSkill "${skillName}" created successfully!`);
  console.log("\nNext steps:");
  console.log(
    `  1. Edit skills/${skillName}/SKILL.md to add your skill content`
  );
  console.log(
    `  2. Update skills/${skillName}/.claude-plugin/plugin.json if needed`
  );
  console.log();
}

main().catch((error) => {
  console.error("Error:", error.message);
  process.exit(1);
});
