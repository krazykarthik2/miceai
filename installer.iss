; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "MiceAI"
#define MyAppVersion "1.9.8.7"
#define MyAppPublisher "krazycorp"
#define MyAppURL "https://karthikkrazy.web.app"
#define MyAppExeName "init.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ""
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt
 
[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{397B197D-4E28-467E-A0E4-F59E10B2F86F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DisableDirPage=yes
ChangesAssociations=yes
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputBaseFilename=miceai-setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\karthikkrazy\zdata\miceai\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\venv\*"; DestDir: "{app}\venv"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\karthikkrazy\zdata\miceai\animation-load.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\init.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\ip_cam.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\main_new.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\readme.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\test_code.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\track_hand.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\karthikkrazy\zdata\miceai\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\karthikkrazy\zdata\miceai\__pycache__\*"; DestDir: "{app}\__pycache__"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""
Root: HKA; Subkey: "Software\Classes\Applications\{#MyAppExeName}\SupportedTypes"; ValueType: string; ValueName: ".myp"; ValueData: ""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

