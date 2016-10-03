
import os
import datetime

import osnap.const
import osnap.util


class MakeNSIS:
    # basic format is from:
    # http://nsis.sourceforge.net/A_simple_installer_with_start_menu_shortcut_and_uninstaller

    def __init__(self, defines, file_path, project_packages=[]):
        self.defines = defines  # ordered dict with the defines
        self.file_path = file_path
        self.project_packages = project_packages
        self.file = None
        # we run this in a special subfolder so designate the installers one level up
        self.installers_folder = os.path.join('..', 'installers')

    def write_line(self, l):
        self.file.write(l)
        self.file.write('\n')

    def write_all(self):
        self.file = open(self.file_path, 'w')
        self.write_line('')
        self.write_line('# *** DO NOT EDIT ***')
        self.write_line('# Programmatically generated by %s on %s.' % (__file__, str(datetime.datetime.now())))
        self.write_line('')
        for define in self.defines:
            self.write_line('!define %s %s' % (define, self.defines[define]))
        self.header()
        self.pages()
        self.admin()
        self.install()
        self.uninstall()
        self.file.close()

    def header(self):
        self.write_line('')
        self.write_line('RequestExecutionLevel admin ;Require admin rights on NT6+ (When UAC is turned on)')
        self.write_line('InstallDir "$PROGRAMFILES\${COMPANYNAME}\${APPNAME}"')
        self.write_line('LicenseData "LICENSE"')
        self.write_line("# This will be in the installer/uninstaller's title bar")
        self.write_line('Name "${COMPANYNAME} - ${APPNAME}"')
        self.write_line('Icon "${APPNAME}.ico"')
        self.write_line('outFile "%s\${APPNAME}_installer.exe"' % self.installers_folder)
        self.write_line('')
        self.write_line('!include LogicLib.nsh')

    def pages(self):
        # child classes can override this if they have a different set of pages
        self.write_line('')
        self.write_line('page license')
        self.write_line('page directory')
        self.write_line('Page instfiles')

    def admin(self):
        self.write_line('')
        self.write_line('!macro VerifyUserIsAdmin')
        self.write_line('UserInfo::GetAccountType')
        self.write_line('pop $0')
        self.write_line('${If} $0 != "admin" ;Require admin rights on NT4+')
        self.write_line('        messageBox mb_iconstop "Administrator rights required!"')
        self.write_line('        setErrorLevel 740 ;ERROR_ELEVATION_REQUIRED')
        self.write_line('        quit')
        self.write_line('${EndIf}')
        self.write_line('!macroend')
        self.write_line('')
        self.write_line('function .onInit')
        self.write_line('	setShellVarContext all')
        self.write_line('	!insertmacro VerifyUserIsAdmin')
        self.write_line('functionEnd')

    def install(self):
        self.write_line('')
        self.write_line('section "install"')
        self.write_line('# Files for the install directory - to build the installer, these should be in the same directory as the install script (this file)')
        self.write_line('setOutPath $INSTDIR')
        self.write_line('# Files added here should be removed by the uninstaller (see section "uninstall")')
        self.write_line('file /r *')

        self.write_line('')
        self.write_line('# Uninstaller - See function un.onInit and section "uninstall" for configuration')
        self.write_line('writeUninstaller "$INSTDIR\\uninstall.exe"')
        self.write_line('')
        self.write_line('# Start Menu')
        self.write_line('createDirectory "$SMPROGRAMS\\${COMPANYNAME}"')
        self.write_line('createShortCut "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk" "$INSTDIR\\${EXENAME}" "" "$INSTDIR\\${APPNAME}.ico"')
        self.write_line('')
        self.write_line('# run on Windows startup')
        self.write_line('WriteRegStr HKEY_LOCAL_MACHINE "Software\\Microsoft\\Windows\\CurrentVersion\\Run" "${APPNAME}" "$INSTDIR\\${EXENAME}"')
        self.write_line('')
        self.write_line('# Registry information for add/remove programs')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayName" "${COMPANYNAME} - ${APPNAME} - ${DESCRIPTION}"')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "UninstallString" "$\\"$INSTDIR\\uninstall.exe$\\""')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "QuietUninstallString" "$\\"$INSTDIR\\uninstall.exe$\\" /S"')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "InstallLocation" "$INSTDIR"')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayIcon" "$\\"$INSTDIR\\logo.ico$\\""')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "Publisher" "${COMPANYNAME}"')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "HelpLink" "${HELPURL}"')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "URLInfoAbout" "${ABOUTURL}"')
        self.write_line('WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"')
        self.write_line('WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMajor" ${VERSIONMAJOR}')
        self.write_line('WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "VersionMinor" ${VERSIONMINOR}')
        self.write_line('WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoModify" 1')
        self.write_line('WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "NoRepair" 1')
        self.write_line('WriteRegDWORD HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}" "EstimatedSize" ${INSTALLSIZE}')
        self.write_line('sectionEnd')

    def uninstall(self):
        self.write_line('# Uninstaller')
        self.write_line('function un.onInit')
        self.write_line('	SetShellVarContext all')

        self.write_line('# Verify the uninstaller - last chance to back out')
        self.write_line('	MessageBox MB_OKCANCEL "Permanantly remove ${APPNAME}?" IDOK next')
        self.write_line('		Abort')
        self.write_line('	next:')
        self.write_line('!insertmacro VerifyUserIsAdmin')
        self.write_line('functionEnd')

        self.write_line('section "uninstall"')

        self.write_line('# Remove Start Menu launcher')
        self.write_line('delete "$SMPROGRAMS\\${COMPANYNAME}\\${APPNAME}.lnk"')
        self.write_line('# Try to remove the Start Menu folder - this will only happen if it is empty')
        self.write_line('rmDir "$SMPROGRAMS\\${COMPANYNAME}"')

        self.write_line('# Remove files')
        self.write_line('RMDir /r $INSTDIR\\%s' % osnap.const.python_folder)
        for project_package in self.project_packages:
            self.write_line('RMDir /r $INSTDIR\\%s' % project_package)
        self.write_line('delete $INSTDIR\\${EXENAME}')
        self.write_line('delete $INSTDIR\\LICENSE')
        self.write_line('delete $INSTDIR\\*.ico')
        self.write_line('delete $INSTDIR\\*.md')
        self.write_line('delete $INSTDIR\\*.py')
        self.write_line('delete $INSTDIR\\*.pyd')
        self.write_line('delete $INSTDIR\\*.exe')

        self.write_line('# Always delete uninstaller as the last action')
        self.write_line('delete $INSTDIR\\uninstall.exe')

        self.write_line('# Try to remove the install directory - this will only happen if it is empty')
        self.write_line('rmDir $INSTDIR')

        self.write_line('# Remove uninstaller information from the registry')
        self.write_line('DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${COMPANYNAME} ${APPNAME}"')
        self.write_line('sectionEnd')


def get_folder_size(folder_path):
    total_size = 0
    for d, _, fns in os.walk(folder_path):
        for f in fns:
            total_size += os.path.getsize(os.path.join(d, f))
    return total_size
