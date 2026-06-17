[Setup]
#define MyAppExeName "NeuraFind.exe"
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
AppId={{D37F2C0B-9B21-4A59-8139-4A8E0C9B6A1A}
AppName=NeuraFind
AppVersion=1.0.0
AppPublisher=Hussein Al-Furati
AppPublisherURL=https://github.com/Hussein-Furaty/NeuraFind
AppSupportURL=https://github.com/Hussein-Furaty/NeuraFind/issues
AppUpdatesURL=https://github.com/Hussein-Furaty/NeuraFind/releases
DefaultDirName={autopf}\NeuraFind
DisableProgramGroupPage=yes
; Display the Bilingual License Agreement (English & Arabic)
LicenseFile=..\docs\LICENSE.txt
; Output directory for the installer executable
OutputDir=..\dist
OutputBaseFilename=NeuraFind_Setup_v1.0.0
SetupIconFile=..\assets\NeuraFind.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "..\dist\NeuraFind\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\dist\NeuraFind\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\NeuraFind"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\NeuraFind"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,NeuraFind}"; Flags: nowait postinstall skipifsilent
