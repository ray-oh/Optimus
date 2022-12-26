Optimus RPA Package

INSTALLATION
- Requires: install-optimus.bat and a optimus_package*.zip file.
- optimus_package is in continuous release and new releases are versioned in YYYYMMDD format.
  It is advisable you use the latest version available.  Check the release notes on what is included in the version.
- Each new release can also be installed over a previous release as an upgrade.  
  Normally, an upgrade installation will not remove existing user files.  But it may overwrite existing scripts files with same name.
  Backup your scripts folder to avoid problems.
- Downloadable from: RPA Project Team Site: 
    https://christiandior.sharepoint.com/:f:/s/Grp_RPAProject-KBQuest/ErGLyzBc3QtKj9WzjxDuik0BsuRiyPJB3DHKq-X091PuOg?e=fmxPRt

USAGE
- Use runRPA.bat to launch RPA program.  Requires to specify an Excel script file.
- Example:   >> runRPA -f main-test  
- Sample script files "main-test" available to test various RPA functionality
- All excel script files are to be placed in \scripts
    And they can include RPA images (for Visual automation of your desktop and websites)

DOCUMENTATION
- Documentation available in: \autobot\docs
- Optimus is based on TagUI for RPA automation.  Almost all of TagUI's features are ported and available in Optimus.
    And some have also been enhanced.
    A good reference for the key RPA features available in Optimus is available from the TagUI official sites, in particular: 
    https://aisingapore.org/tagui/ - official TagUI site.
    And https://github.com/tebelorg/RPA-Python - the python version of TagUI

PROGRAM TECHNICAL INFORMATION
- Pre-requisites:
- Windows 10 and Windows 10 Enterprise Server on VM
- Python 3.9 and above
- Autobot (RPA component) - based on TagUI and various addon python packages
- Prefect (workflow orchestration) - full fledged orchestration package for dataflow automation
    https://www.prefect.io/ - official site
    Currently in pre-Alpha stage for integration with Autobot.

RELEASE NOTES:

20221006 - Stable release
        New features:
        Installation scripts and package updates.
        scripts (user files) folders separated from Autobot program folder.

CONTACT
Raymond Oh - for reporting of bugs, questions, requests etc
