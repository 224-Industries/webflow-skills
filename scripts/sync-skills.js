#!/usr/bin/env node

/**
 * @module sync-skills
 * @description Discovers skills in the skills/ directory and syncs their metadata
 * across all generated files: manifest.json, platform plugin configs
 * (.claude-plugin/plugin.json, .cursor-plugin/plugin.json),
 * .claude-plugin/marketplace.json, skills/index.json, and README.md.
 *
 * Also propagates author and repository from manifest.json into each
 * skill's SKILL.md frontmatter.
 * @example
 * // Run from the repository root
 * node scripts/sync-skills.js
 */

import { mkdir, readdir, readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = join(__dirname, "..");
const SKILLS_DIR = join(ROOT_DIR, "skills");
const README_PATH = join(ROOT_DIR, "README.md");
const MANIFEST_PATH = join(ROOT_DIR, "manifest.json");
const CLAUDE_MARKETPLACE_PATH = join(ROOT_DIR, ".claude-plugin", "marketplace.json");
const CLAUDE_PLUGIN_PATH = join(ROOT_DIR, ".claude-plugin", "plugin.json");
const CURSOR_PLUGIN_PATH = join(ROOT_DIR, ".cursor-plugin", "plugin.json");
const INDEX_PATH = join(SKILLS_DIR, "index.json");

const FRONTMATTER_REGEX = /^---\n([\s\S]*?)\n---/;
const WHITESPACE_REGEX = /\S/;

function parseValue(raw) {
  const trimmed = raw.trim();
  if (trimmed.startsWith("[") && trimmed.endsWith("]")) {
    try {
      return JSON.parse(trimmed);
    } catch {
      return trimmed;
    }
  }
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

      const value = parseValue(rawValue);
      if (value !== "") {
        currentObject[key] = value;
      }
    } else {

      const value = parseValue(rawValue);
      if (value === "") {

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

// Scans the skills/ directory for subdirectories containing a SKILL.md,
// parses each file's frontmatter, and returns a sorted array of skill metadata.
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

    try {
      const skillMd = await readFile(skillMdPath, "utf-8");
      const frontmatter = parseFrontmatter(skillMd);
      const metadata = frontmatter.metadata || {};
      const keywords = typeof metadata.keywords === "string"
        ? metadata.keywords.split(",").map((k) => k.trim()).filter(Boolean)
        : [];

      skills.push({
        dirName: entry.name,
        name: frontmatter.name || entry.name,
        description: frontmatter.description || "",
        license: frontmatter.license || "MIT",
        version: metadata.version || "1.0.0",
        keywords,
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

// Builds a markdown table of skills with links to their directories,
// used to replace the auto-generated section in README.md.
function generateReadmeSkillsList(skills) {
  if (skills.length === 0) {
    return "\n*No skills available yet.*\n";
  }

  const lines = ["", "| Skill | Description | Download |", "| ----- | ----------- | -------- |"];

  for (const skill of skills) {
    const escapedDesc = truncate(skill.description).replace(/\|/g, "\\|");
    const downloadUrl = `https://skills.224ai.au/${skill.dirName}.skill`;
    lines.push(`| [${skill.name}](./skills/${skill.dirName}) | ${escapedDesc} | [Download](${downloadUrl}) |`);
  }

  lines.push("");
  return lines.join("\n");
}

// Replaces the skills table between the START/END markers in README.md
// with a freshly generated table from the current skills list.
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

// Writes the skills array into manifest.json with name, description,
// version, source path, license, and keywords for each skill.
async function updateManifest(manifest, skills) {
  manifest.skills = skills.map((skill) => ({
    name: skill.name,
    description: skill.description,
    version: skill.version,
    source: `./skills/${skill.dirName}`,
    license: skill.license,
    keywords: skill.keywords,
  }));

  await writeFile(
    MANIFEST_PATH,
    `${JSON.stringify(manifest, null, 2)}\n`,
    "utf-8"
  );
}

// Generates a platform plugin.json at the given path from manifest metadata,
// creating the directory if it doesn't exist. Extra fields (e.g. logo) are merged in.
async function updatePlugin(manifest, pluginPath, extraFields = {}) {
  const pluginJson = {
    name: manifest.name,
    description: manifest.description,
    version: manifest.version,
    author: manifest.author,
    homepage: manifest.homepage,
    repository: manifest.repository,
    license: manifest.license,
    keywords: manifest.keywords || [],
    skills: "./skills/",
    ...extraFields,
  };

  await mkdir(dirname(pluginPath), { recursive: true });
  await writeFile(
    pluginPath,
    `${JSON.stringify(pluginJson, null, 2)}\n`,
    "utf-8"
  );
  return true;
}

// Updates .claude-plugin/marketplace.json with the current manifest
// metadata so the plugin is discoverable in the Claude marketplace.
async function updateMarketplace(manifest) {
  let marketplace;
  try {
    const content = await readFile(CLAUDE_MARKETPLACE_PATH, "utf-8");
    marketplace = JSON.parse(content);
  } catch {
    console.warn("Warning: Could not read marketplace.json");
    return false;
  }

  marketplace.plugins = [
    {
      name: manifest.name,
      description: manifest.description,
      version: manifest.version,
      author: manifest.author,
      source: "./",
      homepage: manifest.homepage,
      repository: manifest.repository,
      license: manifest.license,
      keywords: manifest.keywords || [],
    },
  ];

  await writeFile(
    CLAUDE_MARKETPLACE_PATH,
    `${JSON.stringify(marketplace, null, 2)}\n`,
    "utf-8"
  );
  return true;
}

// Recursively walks a skill directory and returns all file paths relative
// to that directory, with SKILL.md sorted first per the RFC spec.
async function listSkillFiles(skillDir) {
  const files = [];

  async function walk(dir, prefix) {
    const entries = await readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      const relativePath = prefix ? `${prefix}/${entry.name}` : entry.name;
      if (entry.isDirectory()) {
        await walk(join(dir, entry.name), relativePath);
      } else {
        files.push(relativePath);
      }
    }
  }

  await walk(skillDir, "");

  // SKILL.md must be first per the RFC spec
  files.sort((a, b) => {
    if (a === "SKILL.md") return -1;
    if (b === "SKILL.md") return 1;
    return a.localeCompare(b);
  });

  return files;
}

// Generates skills/index.json following the agent-skills-discovery RFC,
// listing each skill's name, description, and full file manifest.
async function updateIndex(skills) {
  const indexSkills = await Promise.all(
    skills.map(async (skill) => {
      const skillDir = join(SKILLS_DIR, skill.dirName);
      const files = await listSkillFiles(skillDir);
      return {
        name: skill.dirName,
        description: skill.description,
        files,
      };
    })
  );

  await writeFile(
    INDEX_PATH,
    `${JSON.stringify({ skills: indexSkills }, null, 2)}\n`,
    "utf-8"
  );
  return true;
}

// Propagates author and repository from manifest.json into each
// skill's SKILL.md frontmatter so they stay in sync.
async function updateSkillFrontmatter(skills, manifest) {
  const author = manifest.author?.name || "";
  const repository = manifest.repository || "";
  let updated = 0;

  for (const skill of skills) {
    const skillMdPath = join(SKILLS_DIR, skill.dirName, "SKILL.md");
    let content = await readFile(skillMdPath, "utf-8");
    const original = content;

    if (author) {
      content = content.replace(
        /^(  author:) .+$/m,
        `$1 "${author}"`
      );
    }

    if (repository) {
      if (/^  repository: .+$/m.test(content)) {
        content = content.replace(
          /^(  repository:) .+$/m,
          `$1 "${repository}"`
        );
      } else {
  
        content = content.replace(
          /^(  author: .+)$/m,
          `$1\n  repository: "${repository}"`
        );
      }
    }

    if (content !== original) {
      await writeFile(skillMdPath, content, "utf-8");
      updated++;
    }
  }

  return updated;
}

// Entry point — discovers skills, then updates all generated files
// (manifest, plugins, marketplace, index, README) in sequence.
async function main() {
  console.log("Syncing agent skill(s)...\n");

  const skills = await discoverSkills();
  console.log(`Found ${skills.length} agent skill(s):`);
  for (const skill of skills) {
    console.log(`  - ${skill.name}`);
  }
  console.log();

  const manifest = JSON.parse(await readFile(MANIFEST_PATH, "utf-8"));

  const skillsUpdated = await updateSkillFrontmatter(skills, manifest);
  if (skillsUpdated > 0) {
    console.log(`Updated ${skillsUpdated} SKILL.md file(s)`);
  }

  await updateManifest(manifest, skills);
  console.log("Updated manifest.json");

  await updatePlugin(manifest, CLAUDE_PLUGIN_PATH);
  console.log("Updated .claude-plugin/plugin.json");

  const marketplaceUpdated = await updateMarketplace(manifest);
  if (marketplaceUpdated) {
    console.log("Updated .claude-plugin/marketplace.json");
  }

  await updatePlugin(manifest, CURSOR_PLUGIN_PATH, { logo: manifest.logo });
  console.log("Updated .cursor-plugin/plugin.json");

  const indexUpdated = await updateIndex(skills);
  if (indexUpdated) {
    console.log("Updated skills/index.json");
  }

  const readmeUpdated = await updateReadme(skills);
  if (readmeUpdated) {
    console.log("Updated README.md");
  }

  console.log("\nSkill Sync Complete!");
}

main().catch((error) => {
  console.error("Error:", error.message);
  process.exit(1);
});
