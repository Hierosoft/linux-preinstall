# LibreOffice

## Compatibility
To make LibreOffice behave more like Microsoft Office, you can change
the following settings in the menu bar.

Clock "Tools", "Options" then under:
- LibreOffice Writer
  - General
    - Change "Tab stops" to .5 (.79 default0
  - Grid:
    - Change Horizontal and Vertical each to .25 (.39 default)
      (leave default Subdivision as 2x2)
- LibreOffice Writer/Web
  - Grid:
    - Change Horizontal and Vertical each to .5 (.39 default)
      (since default Subdivision is 4x4)

### Optional compatibility
- LibreOffice Writer
  - Compatibility
    - check "Reorganize Form menu for Microsoft compatibility"
      and possibly other options.

### No longer recommended compatibility
Changing the default formats to Microsoft formats is no longer recommended since:
- Microsoft added open document format compatibility. It is available as an option (from their website) starting around Office 2003 and comes with later versions.
- The default formats may not function correctly such as with headers in Word format or templates and fonts in PowerPoint format.
- In LibreOffice versions released around 2013, saving/loading some Microsoft XML files (Excel or PowerPoint) could crash LibreOffice and/or lose all of the data. However, the reliability seems to have improved since then.

Changing the default formats:
- Load/Save
  - General
    - Document Type:
      - Choose Text Document then next to "Always save as", choose "Word 2007-365 (*.docx)"
      - Choose Spreadsheet then next to "Always save as", choose "Excel 2007-365 (*.xlsx)"
      - Choose Presentation then next to "Always save as", choose "PowerPoint 2007-365 (*.pptx)"
