# Sentinel Ops Suite — Drift Modules  
Modular, deterministic plugin system for drift detection.

---

## Overview

The drift detection engine in the Sentinel Ops Suite is fully modular.  
Each drift collector is implemented as a **plugin** inside this directory.

Plugins are responsible for collecting a specific category of repository state, such as:

- Filesystem hashes  
- Git metadata  
- Environment metadata  
- Dependency manifests  
- Configuration fingerprints  

The drift engine loads plugins in a **deterministic order** defined in:
drift_modules/init.py


This ensures stable, reproducible output across machines and CI environments.

---

## Plugin Requirements

Each plugin must implement:

```python
class PluginName:
    name = "unique_plugin_name"

    def collect(self, root: Path) -> dict:
        ...
Required attributes

Required behavior
• 	Output must be deterministic
• 	Output must be JSON‑serializable
• 	Output must not include timestamps, randomness, or machine‑specific paths
• 	Output must be stable across repeated runs

Current Plugins
1. 
Collects SHA256 hashes of all files in the repository, excluding:
• 	
• 	
• 	
• 	
This provides a deterministic fingerprint of the entire codebase.
2. 
Collects minimal Git metadata:
• 	Current branch
• 	Current commit
• 	Working tree cleanliness
• 	List of modified files
This ensures drift detection captures both file changes and Git state changes.

Adding a New Plugin
1. 	Create a new file in this directory:

2. 	Implement the plugin:

3. 	Register it in:

Example:

4. 	Run:

Verify that:
• 	Output is deterministic
• 	No nondeterministic fields appear
• 	CI drift checks behave correctly

Best Practices
• 	Avoid timestamps
• 	Avoid absolute paths
• 	Avoid randomness
• 	Avoid machine‑specific metadata
• 	Keep output small and structured
• 	Use sorted lists and sorted dict keys
• 	Ensure plugin output is stable across runs

Summary
The drift module system provides:
• 	Clean separation of drift collectors
• 	Deterministic plugin ordering
• 	Extensibility for future drift domains
• 	CI‑ready, operator‑grade behavior
Plugins are simple, powerful, and designed for forensic‑grade drift detection.
