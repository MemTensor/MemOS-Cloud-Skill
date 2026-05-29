#!/usr/bin/env node

import { readFileSync } from "node:fs";
import { writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const rootDir = resolve(__dirname, "..");
const skillDir = "memos-cloud-server";
const packageJsonPath = resolve(rootDir, "package.json");
const pyprojectPath = resolve(rootDir, "pyproject.toml");
const runtimeInitPath = resolve(rootDir, skillDir, "scripts", "memos_cloud", "__init__.py");
const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf8"));

const options = parseArgs(process.argv.slice(2));
const channel = options.channel ?? "latest";
const version = options.version ?? nextVersion(packageJson.version, channel);
const slug = options.slug ?? "memos-cloud-server";
const displayName = options.name ?? "MemOS Cloud Server";
const npmTag = options.npmTag ?? channel;
const clawhubTags = options.clawhubTags ?? channel;
const changelog = options.changelog ?? `Release ${version}`;
const clawscanNote =
  options.clawscanNote ??
  "Uses network access only to call the user-configured MemOS Cloud API. Reads MEMOS_API_KEY, MEMOS_USER_ID, and MEMOS_CLOUD_URL from environment variables.";

main();

function main() {
  validateChannel(channel);
  syncVersions(version, { dryRun: options.dryRun });

  if (!options.skipTests) {
    run("uv", ["run", "pytest"]);
    run("uv", ["run", "python", `${skillDir}/scripts/memos_cloud.py`, "--help"]);
  }

  if (!options.skipNpm) {
    if (options.dryRun) {
      run("npm", ["pack", "--dry-run"]);
    } else {
      run("npm", ["publish", "--tag", npmTag]);
    }
  }

  if (!options.skipClawhub) {
    if (options.dryRun) {
      run("clawhub", ["sync", "--root", "./memos-cloud-server", "--all", "--dry-run"]);
    } else {
      run("clawhub", [
        "skill",
        "publish",
        `./${skillDir}`,
        "--slug",
        slug,
        "--name",
        displayName,
        "--version",
        version,
        "--tags",
        clawhubTags,
        "--changelog",
        changelog,
        "--clawscan-note",
        clawscanNote,
      ]);
    }
  }
}

function parseArgs(args) {
  const parsed = {
    dryRun: false,
    skipTests: false,
    skipNpm: false,
    skipClawhub: false,
  };

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    switch (arg) {
      case "--dry-run":
        parsed.dryRun = true;
        break;
      case "--skip-tests":
        parsed.skipTests = true;
        break;
      case "--skip-npm":
        parsed.skipNpm = true;
        break;
      case "--skip-clawhub":
        parsed.skipClawhub = true;
        break;
      case "--channel":
        parsed.channel = readValue(args, (index += 1), arg);
        break;
      case "--npm-tag":
        parsed.npmTag = readValue(args, (index += 1), arg);
        break;
      case "--clawhub-tags":
        parsed.clawhubTags = readValue(args, (index += 1), arg);
        break;
      case "--version":
        parsed.version = readValue(args, (index += 1), arg);
        break;
      case "--slug":
        parsed.slug = readValue(args, (index += 1), arg);
        break;
      case "--name":
        parsed.name = readValue(args, (index += 1), arg);
        break;
      case "--changelog":
        parsed.changelog = readValue(args, (index += 1), arg);
        break;
      case "--clawscan-note":
        parsed.clawscanNote = readValue(args, (index += 1), arg);
        break;
      default:
        usage(`Unknown option: ${arg}`);
    }
  }

  return parsed;
}

function validateChannel(value) {
  if (!["latest", "beta"].includes(value)) {
    usage(`Invalid channel: ${value}. Expected "latest" or "beta".`);
  }
}

function nextVersion(currentVersion, releaseChannel) {
  const parsed = parseSemver(currentVersion);

  if (releaseChannel === "beta") {
    const betaMatch = parsed.prerelease?.match(/^beta\.(\d+)$/);
    if (betaMatch) {
      return `${parsed.major}.${parsed.minor}.${parsed.patch}-beta.${Number(betaMatch[1]) + 1}`;
    }
    return `${parsed.major}.${parsed.minor}.${parsed.patch + 1}-beta.0`;
  }

  if (parsed.prerelease) {
    return `${parsed.major}.${parsed.minor}.${parsed.patch}`;
  }

  return `${parsed.major}.${parsed.minor}.${parsed.patch + 1}`;
}

function parseSemver(value) {
  const match = value.match(/^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$/);
  if (!match) {
    usage(`Invalid semver version in package.json: ${value}`);
  }

  return {
    major: Number(match[1]),
    minor: Number(match[2]),
    patch: Number(match[3]),
    prerelease: match[4],
  };
}

function syncVersions(next, { dryRun }) {
  console.error(`\n> version ${packageJson.version} -> ${next}${dryRun ? " (dry run)" : ""}`);

  if (dryRun) {
    return;
  }

  packageJson.version = next;
  writeFileSync(packageJsonPath, `${JSON.stringify(packageJson, null, 4)}\n`);

  const pyproject = readFileSync(pyprojectPath, "utf8");
  const updatedPyproject = pyproject.replace(
    /^version = "([^"]+)"/m,
    `version = "${next}"`,
  );

  if (updatedPyproject === pyproject) {
    usage("Could not find project version in pyproject.toml");
  }

  writeFileSync(pyprojectPath, updatedPyproject);

  const runtimeInit = readFileSync(runtimeInitPath, "utf8");
  const updatedRuntimeInit = runtimeInit.replace(
    /^__version__ = "([^"]+)"/m,
    `__version__ = "${next}"`,
  );

  if (updatedRuntimeInit === runtimeInit) {
    usage("Could not find __version__ in runtime package");
  }

  writeFileSync(runtimeInitPath, updatedRuntimeInit);
}

function readValue(args, index, flag) {
  const value = args[index];
  if (!value || value.startsWith("--")) {
    usage(`Missing value for ${flag}`);
  }
  return value;
}

function run(command, args) {
  const display = [command, ...args].join(" ");
  console.error(`\n> ${display}`);
  const result = spawnSync(command, args, {
    cwd: rootDir,
    stdio: "inherit",
    shell: process.platform === "win32",
  });

  if (result.error) {
    console.error(`Failed to run ${command}: ${result.error.message}`);
    process.exit(1);
  }

  if (result.status !== 0) {
    console.error(`Command failed with exit code ${result.status}: ${display}`);
    process.exit(result.status ?? 1);
  }
}

function usage(message) {
  console.error(message);
  console.error(`
Usage: node tools/publish.mjs [options]

Options:
  --dry-run
  --skip-tests
  --skip-npm
  --skip-clawhub
  --channel <latest|beta>
  --npm-tag <tag>
  --clawhub-tags <tags>
  --version <semver>
  --slug <slug>
  --name <display-name>
  --changelog <text>
  --clawscan-note <text>
`);
  process.exit(1);
}
