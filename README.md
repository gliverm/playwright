# playwright

Intended to be exploritory into playwright GUI automation

## Development Environment

This section describes the project's development environment turn up.  The project is intended to be developed within a docker container to decouple as much as possible from the underlying host.  

## Environment Prerequisites

Pre-requistes on the host include: 

*  Docker
*  Git
*  Visual Studio Code (VSCode) IDE
*  Host MacOS - currently being developed using MacOS
*  X Window System - on MacOS install XQuartz

### XQuartz Installation

These steps make the assumption the MacOS host has homebrew installed.

1. brew update
2. brew upgrade
3. brew install --cask xquartz
4. (untested steps)


## Starting Playwright Codegen

From the pipenv shell from within the development container: `playwright codegen test-url`

Example: `playwright codegen --ignore-https-errors https://10.136.1.31:3443/smx`

## Other Notes 

*  GUI web testing at top of testing pyramid - time consuming and brittle in comparision to pure API and backend testing.
*  