#!/usr/bin/env node

/**
 * sync-skills.js
 *
 * Syncs the Available Skills section in README.md and the plugins array
 * in .claude-plugin/marketplace.json with the actual skills in skills/
 *
 * Usage: node scripts/sync-skills.js
 */

import { readdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = join(__dirname, "..");
const SKILLS_DIR = join(ROOT_DIR, "skills");
const README_PATH = join(ROOT_DIR, "README.md");
const MARKETPLACE_PATH = join(ROOT_DIR, ".claude-plugin", "marketplace.json");

const FRONTMATTER_REGEX = /^---\n([\s\S]*?)\n---/;
const WHITESPACE_REGEX = /\S/;

function parseValue(raw) {
  const trimmed = raw.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"')) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'"))
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

function parseFrontmatter(content) {
  const match = content.match(FRONTMATTER_REGEX);
  if (!match) {
    return {};
  }

  const lines = match[1].split("\n");
  const result = {};
  let currentObject = null;

  for (const line of lines) {
    if (line.trim() === "") {
      continue;
    }

    const colonIndex = line.indexOf(":");
    if (colonIndex === -1) {
      continue;
    }

    const indent = line.search(WHITESPACE_REGEX);
    const key = line.slice(0, colonIndex).trim();
    const rawValue = line.slice(colonIndex + 1);

    if (indent > 0 && currentObject !== null) {
      // Nested property
      const value = parseValue(rawValue);
      if (value !== "") {
        currentObject[key] = value;
      }
    } else {
      // Top-level property
      const value = parseValue(rawValue);
      if (value === "") {
        // Start of a nested object
        currentObject = {};
        result[key] = currentObject;
      } else {
        currentObject = null;
        result[key] = value;
      }
    }
  }

  return result;
}

async function discoverSkills() {
  const skills = [];

  let entries;
  try {
    entries = await readdir(SKILLS_DIR, { withFileTypes: true });
  } catch {
    console.warn("No skills directory found. Skipping sync.");
    return skills;
  }

  for (const entry of entries) {
    if (!entry.isDirectory()) {
      continue;
    }

    const skillDir = join(SKILLS_DIR, entry.name);
    const skillMdPath = join(skillDir, "SKILL.md");
    const pluginJsonPath = join(skillDir, ".claude-plugin", "plugin.json");

    try {
      const skillMd = await readFile(skillMdPath, "utf-8");
      const frontmatter = parseFrontmatter(skillMd);

      let pluginJson = {};
      try {
        const pluginContent = await readFile(pluginJsonPath, "utf-8");
        pluginJson = JSON.parse(pluginContent);
      } catch {
        // Ignore missing or invalid plugin.json
      }

      const metadata = frontmatter.metadata || {};

      skills.push({
        dirName: entry.name,
        name: frontmatter.name || entry.name,
        description: frontmatter.description || pluginJson.description || "",
        license: frontmatter.license || pluginJson.license || "MIT",
        version: metadata.version || pluginJson.version || "1.0.0",
        author: pluginJson.author || {},
        homepage: pluginJson.homepage || "",
        repository: pluginJson.repository || "",
        keywords: pluginJson.keywords || [],
      });
    } catch (error) {
      console.warn(
        `Warning: Could not read skill at ${entry.name}:`,
        error.message
      );
    }
  }

  return skills.sort((a, b) => a.name.localeCompare(b.name));
}

function truncate(str, maxLength = 80) {
  if (str.length <= maxLength) {
    return str;
  }
  return `${str.slice(0, maxLength - 3)}...`;
}

function generateReadmeSkillsList(skills) {
  if (skills.length === 0) {
    return "\n*No skills available yet.*\n";
  }

  const lines = ["", "| Skill | Description |", "| ----- | ----------- |"];

  for (const skill of skills) {
    const escapedDesc = truncate(skill.description).replace(/\|/g, "\\|");
    lines.push(`| [${skill.name}](./skills/${skill.dirName}) | ${escapedDesc} |`);
  }

  lines.push("");
  return lines.join("\n");
}

async function updateReadme(skills) {
  const content = await readFile(README_PATH, "utf-8");
  const startMarker = "<!-- START:Available-Skills -->";
  const endMarker = "<!-- END:Available-Skills -->";

  const startIndex = content.indexOf(startMarker);
  const endIndex = content.indexOf(endMarker);

  if (startIndex === -1 || endIndex === -1) {
    console.warn("Warning: Could not find skill markers in README.md");
    return false;
  }

  const skillsList = generateReadmeSkillsList(skills);
  const newContent =
    content.slice(0, startIndex + startMarker.length) +
    skillsList +
    content.slice(endIndex);

  await writeFile(README_PATH, newContent, "utf-8");
  return true;
}

async function updateMarketplace(skills) {
  let marketplace;
  try {
    const content = await readFile(MARKETPLACE_PATH, "utf-8");
    marketplace = JSON.parse(content);
  } catch {
    console.warn("Warning: Could not read marketplace.json");
    return false;
  }

  marketplace.plugins = skills.map((skill) => ({
    name: `${skill.name}-skill`,
    description: skill.description,
    version: skill.version,
    author: skill.author,
    source: `./skills/${skill.dirName}`,
    homepage: skill.homepage,
    repository: skill.repository,
    license: skill.license,
    keywords: skill.keywords,
  }));

  await writeFile(
    MARKETPLACE_PATH,
    `${JSON.stringify(marketplace, null, 2)}\n`,
    "utf-8"
  );
  return true;
}

async function updatePluginJson(skills) {
  let updated = 0;

  for (const skill of skills) {
    const pluginJsonPath = join(SKILLS_DIR, skill.dirName, ".claude-plugin", "plugin.json");

    let pluginJson;
    try {
      const content = await readFile(pluginJsonPath, "utf-8");
      pluginJson = JSON.parse(content);
    } catch {
      continue;
    }

    let changed = false;

    const pluginName = `${skill.name}-skill`;
    if (pluginJson.name !== pluginName) {
      pluginJson.name = pluginName;
      changed = true;
    }

    if (pluginJson.description !== skill.description) {
      pluginJson.description = skill.description;
      changed = true;
    }

    if (skill.version && pluginJson.version !== skill.version) {
      pluginJson.version = skill.version;
      changed = true;
    }

    if (changed) {
      await writeFile(pluginJsonPath, `${JSON.stringify(pluginJson, null, 2)}\n`, "utf-8");
      updated++;
    }
  }

  return updated;
}

async function main() {
  console.log("Syncing agent skill(s)...\n");

  const skills = await discoverSkills();
  console.log(`Found ${skills.length} agent skill(s):`);
  for (const skill of skills) {
    console.log(`  - ${skill.name}`);
  }
  console.log();

  const pluginCount = await updatePluginJson(skills);
  if (pluginCount > 0) {
    console.log(`✓ Updated ${pluginCount} plugin.json file(s)`);
  }

  const readmeUpdated = await updateReadme(skills);
  if (readmeUpdated) {
    console.log("✓ Updated README.md");
  }

  const marketplaceUpdated = await updateMarketplace(skills);
  if (marketplaceUpdated) {
    console.log("✓ Updated .claude-plugin/marketplace.json");
  }

  console.log("\nDone!");
}

main().catch((error) => {
  console.error("Error:", error.message);
  process.exit(1);
});
