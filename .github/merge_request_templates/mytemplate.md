## Purpose
- Why you did what you did.

## How To Test
- Where reviewers can see your changes. What they should attempt to do.

## What Changed
- What changed in what you did.

## Notes
- Ticket ID (link Jira or taskID)

## Pre-MR Checklist
- [X] Branch name: 
  - [X] Ensure it is correct and has the appropriate prefix (feature/fix/update/…)
  - [X] Contains the module/feature name, subtask title… briefly
  - [X] For bug fixes, include the bug ID as a suffix.
- [X] Commit comment:\
A branch can have multiple commits if the code volume relates to multiple parts (many functions) or many steps; each part and step should be separated into different commits. Each commit's comment should briefly state:
  - [X] The part that was modified
  - [X] The content of the modification
- [X] Reducing code changes:
  - [X] Limit changes to parts unrelated to your task.
  - [X] Only commit the code parts you intended to modify; even if there are spelling or formatting errors in other parts, leave them unchanged instead of fixing them just because it is convenient.
- [X] Coding convention/coding format:
  - [X] Only apply coding format to the files/parts of the code you modified, do not apply coding format to the entire source code to avoid unnecessary changes.
  - [X] If there are too many coding format errors, report it so that a separate MR/commit can be created to fix them.
- [X] Typo/grammar mistakes:
  - [X] For parts related to UI/language/user-displayed messages, ensure they match the design/description documents.
  - [X] If there are spelling or grammatical errors, report them to confirm and make appropriate changes before committing.
  - [X] For variable names in the code, avoid long or semantically incorrect names and ensure consistency.
  - [X] When fixing these errors in code, be careful and use the “replace” feature instead of copy & paste or manual typing to avoid missing changes.
- [X] Run Dev/Run Build to Smoke Test locally:
  - [X] Run commands to self-test the features you modified locally and possibly related features to ensure they still work as before.
  - [X] For new features, ensure that when `run build` and `run dev`, the output is consistent.
  - [X] For cases without test cases:
    - [X] Ensure the UI displays as per the design
    - [X] Ensure the feature functions as described in the spec
    - [X] Ensure there are no obvious bugs during common workflow operations